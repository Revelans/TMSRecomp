// Camera motion vectors for the temporal upscaler (AMD FSR 3), built with Ryujinx's SPIR-V builder (Spv.Generator, MIT).
// Our own code. Per pixel: the scene depth d gives the pixel's point in NDC (NVN: +Y up = the top row, z = 2d - 1);
// M = previous view-projection x inverse(current view-projection) (computed on the CPU) takes it to the previous frame's
// NDC; the motion vector is previous pixel position - current pixel position (pixels, jitter removed), the FSR 3
// convention (motionVectorScale 1, 1). Moving characters get the camera motion only (no per-object motion yet).
// The depth is also copied to an R32 float image (the upscaler's depth input).
//   set 0: binding 0 sampled depth (combined image sampler, depth view), binding 1 storage image out mv (rg16f),
//          binding 2 storage image out depth (r32f)
//   push constants: float M[16] (row-major), int width, int height, float jitter x, float jitter y; local size 8 x 8
using Spv.Generator;
using static Spv.Specification;

static class Motion
{
    public static byte[] Build()
    {
        var m = new Module(0x00010300);
        m.AddCapability(Capability.Shader);
        m.AddCapability(Capability.StorageImageExtendedFormats);  // rg16f storage
        m.SetMemoryModel(AddressingModel.Logical, MemoryModel.GLSL450);

        var tVoid = m.TypeVoid();
        var tF = m.TypeFloat(32);
        var tI = m.TypeInt(32, 1);
        var tU = m.TypeInt(32, 0);
        var tB = m.TypeBool();
        var tV4 = m.TypeVector(tF, 4);
        var tI2 = m.TypeVector(tI, 2);
        var tU3 = m.TypeVector(tU, 3);
        var tSrc = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 1, ImageFormat.Unknown);
        var tMv = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 2, ImageFormat.Rg16f);
        var tDep = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 2, ImageFormat.R32f);
        var pSrc = m.TypePointer(StorageClass.UniformConstant, tSrc);
        var pMv = m.TypePointer(StorageClass.UniformConstant, tMv);
        var pDep = m.TypePointer(StorageClass.UniformConstant, tDep);
        var members = new Instruction[20];
        for (int i = 0; i < 16; i++) members[i] = tF;
        members[16] = tI; members[17] = tI; members[18] = tF; members[19] = tF;
        var tPc = m.TypeStruct(true, members);
        var pPc = m.TypePointer(StorageClass.PushConstant, tPc);
        var pPcI = m.TypePointer(StorageClass.PushConstant, tI);
        var pPcF = m.TypePointer(StorageClass.PushConstant, tF);
        var pIn = m.TypePointer(StorageClass.Input, tU3);

        var src = m.Variable(pSrc, StorageClass.UniformConstant);
        var mv = m.Variable(pMv, StorageClass.UniformConstant);
        var dep = m.Variable(pDep, StorageClass.UniformConstant);
        var pc = m.Variable(pPc, StorageClass.PushConstant);
        var gid = m.Variable(pIn, StorageClass.Input);
        m.Decorate(src, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(src, Decoration.Binding, (LiteralInteger)0);
        m.Decorate(mv, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(mv, Decoration.Binding, (LiteralInteger)1);
        m.Decorate(mv, Decoration.NonReadable);
        m.Decorate(dep, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(dep, Decoration.Binding, (LiteralInteger)2);
        m.Decorate(dep, Decoration.NonReadable);
        m.Decorate(gid, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.GlobalInvocationId);
        m.Decorate(tPc, Decoration.Block);
        for (int i = 0; i < 20; i++) m.MemberDecorate(tPc, i, Decoration.Offset, (LiteralInteger)(4 * i));
        foreach (var v in new[] { src, mv, dep, pc, gid }) m.AddGlobalVariable(v);

        Instruction I(int v) => m.Constant(tI, v);
        Instruction F(float v) => m.Constant(tF, v);
        var f0 = F(0f);
        var f1 = F(1f);
        var f2 = F(2f);
        var fHalf = F(0.5f);

        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        m.AddFunction(main);
        m.AddLabel(m.Label());
        var w = m.Load(tI, m.AccessChain(pPcI, pc, I(16)));
        var h = m.Load(tI, m.AccessChain(pPcI, pc, I(17)));
        var jx = m.Load(tF, m.AccessChain(pPcF, pc, I(18)));
        var jy = m.Load(tF, m.AccessChain(pPcF, pc, I(19)));
        var id3 = m.Load(tU3, gid);
        var x = m.Bitcast(tI, m.CompositeExtract(tU, id3, 0));
        var y = m.Bitcast(tI, m.CompositeExtract(tU, id3, 1));
        var inside = m.LogicalAnd(tB, m.SLessThan(tB, x, w), m.SLessThan(tB, y, h));
        var body = m.Label();
        var end = m.Label();
        m.SelectionMerge(end, SelectionControlMask.MaskNone);
        m.BranchConditional(inside, body, end);
        m.AddLabel(body);
        var p = m.CompositeConstruct(tI2, x, y);
        var d = m.CompositeExtract(tF, m.ImageFetch(tV4, m.Load(tSrc, src), p, ImageOperandsMask.Lod, I(0)), 0);
        var wf = m.ConvertSToF(tF, w);
        var hf = m.ConvertSToF(tF, h);
        // pixel centre without the jitter (the depth was drawn with it)
        var px = m.FSub(tF, m.FAdd(tF, m.ConvertSToF(tF, x), fHalf), jx);
        var py = m.FSub(tF, m.FAdd(tF, m.ConvertSToF(tF, y), fHalf), jy);
        var nx = m.FSub(tF, m.FMul(tF, m.FDiv(tF, px, wf), f2), f1);
        var ny = m.FSub(tF, f1, m.FMul(tF, m.FDiv(tF, py, hf), f2));
        var nz = m.FSub(tF, m.FMul(tF, d, f2), f1);
        Instruction M(int r, int c) => m.Load(tF, m.AccessChain(pPcF, pc, I(4 * r + c)));
        Instruction Row(int r) => m.FAdd(tF, m.FAdd(tF, m.FMul(tF, M(r, 0), nx), m.FMul(tF, M(r, 1), ny)),
                                         m.FAdd(tF, m.FMul(tF, M(r, 2), nz), M(r, 3)));
        var qx = Row(0);
        var qy = Row(1);
        var qw = Row(3);
        var ok = m.FOrdGreaterThan(tB, qw, F(1e-6f));
        var safeW = m.Select(tF, ok, qw, f1);
        var ppx = m.FMul(tF, m.FMul(tF, m.FAdd(tF, m.FDiv(tF, qx, safeW), f1), fHalf), wf);
        var ppy = m.FMul(tF, m.FMul(tF, m.FSub(tF, f1, m.FDiv(tF, qy, safeW)), fHalf), hf);
        var mx = m.Select(tF, ok, m.FSub(tF, ppx, px), f0);
        var my = m.Select(tF, ok, m.FSub(tF, ppy, py), f0);
        m.ImageWrite(m.Load(tMv, mv), p, m.CompositeConstruct(tV4, mx, my, f0, f0), ImageOperandsMask.MaskNone);
        m.ImageWrite(m.Load(tDep, dep), p, m.CompositeConstruct(tV4, d, f0, f0, f0), ImageOperandsMask.MaskNone);
        m.Branch(end);
        m.AddLabel(end);
        m.Return();
        m.FunctionEnd();
        m.AddEntryPoint(ExecutionModel.GLCompute, main, "main", gid);
        m.AddExecutionMode(main, ExecutionMode.LocalSize, (LiteralInteger)8, (LiteralInteger)8, (LiteralInteger)1);
        return m.Generate();
    }
}

// Debug check of the motion vectors (NX_MV_CHECK=1): out = 4 x |current - previous frame at (pixel + mv)| (nearest
// texel; dark where the vectors are right), mode 2 = the same without the vectors (for comparison).
//   set 0: binding 0 current colour, binding 1 previous colour, binding 2 mv (combined image samplers, texel fetch),
//          binding 3 storage image out (r11g11b10 float)
//   push constants: int width, int height, int mode; local size 8 x 8
static class MvCheck
{
    public static byte[] Build()
    {
        var m = new Module(0x00010300);
        m.AddCapability(Capability.Shader);
        m.AddCapability(Capability.StorageImageExtendedFormats);
        m.SetMemoryModel(AddressingModel.Logical, MemoryModel.GLSL450);
        var tVoid = m.TypeVoid();
        var tF = m.TypeFloat(32);
        var tI = m.TypeInt(32, 1);
        var tU = m.TypeInt(32, 0);
        var tB = m.TypeBool();
        var tV4 = m.TypeVector(tF, 4);
        var tI2 = m.TypeVector(tI, 2);
        var tU3 = m.TypeVector(tU, 3);
        var tSrc = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 1, ImageFormat.Unknown);
        var tDst = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 2, ImageFormat.R11fG11fB10f);
        var pSrc = m.TypePointer(StorageClass.UniformConstant, tSrc);
        var pDst = m.TypePointer(StorageClass.UniformConstant, tDst);
        var tPc = m.TypeStruct(true, tI, tI, tF);
        var pPc = m.TypePointer(StorageClass.PushConstant, tPc);
        var pPcI = m.TypePointer(StorageClass.PushConstant, tI);
        var pPcF = m.TypePointer(StorageClass.PushConstant, tF);
        var pIn = m.TypePointer(StorageClass.Input, tU3);
        var cur = m.Variable(pSrc, StorageClass.UniformConstant);
        var prev = m.Variable(pSrc, StorageClass.UniformConstant);
        var mv = m.Variable(pSrc, StorageClass.UniformConstant);
        var dst = m.Variable(pDst, StorageClass.UniformConstant);
        var pc = m.Variable(pPc, StorageClass.PushConstant);
        var gid = m.Variable(pIn, StorageClass.Input);
        int bi = 0;
        foreach (var v in new[] { cur, prev, mv, dst })
        {
            m.Decorate(v, Decoration.DescriptorSet, (LiteralInteger)0);
            m.Decorate(v, Decoration.Binding, (LiteralInteger)bi++);
        }
        m.Decorate(dst, Decoration.NonReadable);
        m.Decorate(gid, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.GlobalInvocationId);
        m.Decorate(tPc, Decoration.Block);
        for (int i = 0; i < 3; i++) m.MemberDecorate(tPc, i, Decoration.Offset, (LiteralInteger)(4 * i));
        foreach (var v in new[] { cur, prev, mv, dst, pc, gid }) m.AddGlobalVariable(v);
        Instruction I(int v) => m.Constant(tI, v);
        Instruction F(float v) => m.Constant(tF, v);
        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        m.AddFunction(main);
        m.AddLabel(m.Label());
        var w = m.Load(tI, m.AccessChain(pPcI, pc, I(0)));
        var h = m.Load(tI, m.AccessChain(pPcI, pc, I(1)));
        var scale = m.Load(tF, m.AccessChain(pPcF, pc, I(2)));
        var id3 = m.Load(tU3, gid);
        var x = m.Bitcast(tI, m.CompositeExtract(tU, id3, 0));
        var y = m.Bitcast(tI, m.CompositeExtract(tU, id3, 1));
        var inside = m.LogicalAnd(tB, m.SLessThan(tB, x, w), m.SLessThan(tB, y, h));
        var body = m.Label();
        var end = m.Label();
        m.SelectionMerge(end, SelectionControlMask.MaskNone);
        m.BranchConditional(inside, body, end);
        m.AddLabel(body);
        var p = m.CompositeConstruct(tI2, x, y);
        Instruction Fetch(Instruction img, Instruction q) => m.ImageFetch(tV4, m.Load(tSrc, img), q, ImageOperandsMask.Lod, I(0));
        var c = Fetch(cur, p);
        var v4 = Fetch(mv, p);
        var mx = m.FMul(tF, m.CompositeExtract(tF, v4, 0), scale);
        var my = m.FMul(tF, m.CompositeExtract(tF, v4, 1), scale);
        // bilinear from the previous frame at (pixel + mv)
        var fx = m.FAdd(tF, m.ConvertSToF(tF, x), mx);
        var fy = m.FAdd(tF, m.ConvertSToF(tF, y), my);
        var x0f = m.GlslFloor(tF, fx);
        var y0f = m.GlslFloor(tF, fy);
        var ax = m.FSub(tF, fx, x0f);
        var ay = m.FSub(tF, fy, y0f);
        var x0 = m.ConvertFToS(tI, x0f);
        var y0 = m.ConvertFToS(tI, y0f);
        var z2 = m.ConstantComposite(tI2, I(0), I(0));
        var max2 = m.CompositeConstruct(tI2, m.ISub(tI, w, I(1)), m.ISub(tI, h, I(1)));
        Instruction At(Instruction qx, Instruction qy) => Fetch(prev, m.GlslSClamp(tI2, m.CompositeConstruct(tI2, qx, qy), z2, max2));
        var x1 = m.IAdd(tI, x0, I(1));
        var y1 = m.IAdd(tI, y0, I(1));
        var top = m.GlslFMix(tV4, At(x0, y0), At(x1, y0), m.CompositeConstruct(tV4, ax, ax, ax, ax));
        var bot = m.GlslFMix(tV4, At(x0, y1), At(x1, y1), m.CompositeConstruct(tV4, ax, ax, ax, ax));
        var o = m.GlslFMix(tV4, top, bot, m.CompositeConstruct(tV4, ay, ay, ay, ay));
        var f4 = F(4f);
        var d = m.VectorTimesScalar(tV4, m.GlslFAbs(tV4, m.FSub(tV4, c, o)), f4);
        m.ImageWrite(m.Load(tDst, dst), p, d, ImageOperandsMask.MaskNone);
        m.Branch(end);
        m.AddLabel(end);
        m.Return();
        m.FunctionEnd();
        m.AddEntryPoint(ExecutionModel.GLCompute, main, "main", gid);
        m.AddExecutionMode(main, ExecutionMode.LocalSize, (LiteralInteger)8, (LiteralInteger)8, (LiteralInteger)1);
        return m.Generate();
    }
}
