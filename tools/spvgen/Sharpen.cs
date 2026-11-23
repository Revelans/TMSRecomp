// Contrast-adaptive sharpening compute shader for the runtime's present path, built here with Ryujinx's SPIR-V
// builder (Spv.Generator, MIT) because no GLSL/HLSL -> SPIR-V compiler is available. Our own formulation of the
// usual idea: per channel, the 4 cross neighbours pull the centre away from their mean by a weight that shrinks
// where the local range is already near 0 or 1 (no halos on hard edges).
//   set 0 binding 0: sampled image (the game's frame), binding 1: storage image (the output, R8G8B8A8_UNORM)
//   push constants: int width, int height, float peak (negative: -1/8 light .. -1/5 strong)
//   local size 8 x 8; out = (e + w * (b + d + f + h)) / (1 + 4w), w = peak * sqrt(clamp(min(mn, 1 - mx) / mx))
using Spv.Generator;
using static Spv.Specification;

static class Sharpen
{
    public static byte[] Build()
    {
        var m = new Module(0x00010300);
        m.AddCapability(Capability.Shader);
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
        var tDst = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 2, ImageFormat.Rgba8);
        var pSrc = m.TypePointer(StorageClass.UniformConstant, tSrc);
        var pDst = m.TypePointer(StorageClass.UniformConstant, tDst);
        var tPc = m.TypeStruct(true, tI, tI, tF);
        var pPc = m.TypePointer(StorageClass.PushConstant, tPc);
        var pPcI = m.TypePointer(StorageClass.PushConstant, tI);
        var pPcF = m.TypePointer(StorageClass.PushConstant, tF);
        var pIn = m.TypePointer(StorageClass.Input, tU3);

        var src = m.Variable(pSrc, StorageClass.UniformConstant);
        var dst = m.Variable(pDst, StorageClass.UniformConstant);
        var pc = m.Variable(pPc, StorageClass.PushConstant);
        var gid = m.Variable(pIn, StorageClass.Input);
        m.Decorate(src, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(src, Decoration.Binding, (LiteralInteger)0);
        m.Decorate(dst, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(dst, Decoration.Binding, (LiteralInteger)1);
        m.Decorate(dst, Decoration.NonReadable);
        m.Decorate(gid, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.GlobalInvocationId);
        m.Decorate(tPc, Decoration.Block);
        m.MemberDecorate(tPc, 0, Decoration.Offset, (LiteralInteger)0);
        m.MemberDecorate(tPc, 1, Decoration.Offset, (LiteralInteger)4);
        m.MemberDecorate(tPc, 2, Decoration.Offset, (LiteralInteger)8);
        foreach (var v in new[] { src, dst, pc, gid }) m.AddGlobalVariable(v);

        var i0 = m.Constant(tI, 0);
        var i1 = m.Constant(tI, 1);
        var i2 = m.Constant(tI, 2);
        var f0 = m.Constant(tF, 0f);
        var f1 = m.Constant(tF, 1f);
        var f4 = m.Constant(tF, 4f);
        var fEps = m.Constant(tF, 1f / 1024);
        var v0 = m.ConstantComposite(tV4, f0, f0, f0, f0);
        var v1 = m.ConstantComposite(tV4, f1, f1, f1, f1);
        var vEps = m.ConstantComposite(tV4, fEps, fEps, fEps, fEps);
        var z2 = m.ConstantComposite(tI2, i0, i0);

        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        m.AddFunction(main);
        m.AddLabel(m.Label());
        var w = m.Load(tI, m.AccessChain(pPcI, pc, i0));
        var h = m.Load(tI, m.AccessChain(pPcI, pc, i1));
        var peak = m.Load(tF, m.AccessChain(pPcF, pc, i2));
        var id3 = m.Load(tU3, gid);
        var x = m.Bitcast(tI, m.CompositeExtract(tU, id3, 0));
        var y = m.Bitcast(tI, m.CompositeExtract(tU, id3, 1));
        var inside = m.LogicalAnd(tB, m.SLessThan(tB, x, w), m.SLessThan(tB, y, h));
        var body = m.Label();
        var end = m.Label();
        m.SelectionMerge(end, SelectionControlMask.MaskNone);
        m.BranchConditional(inside, body, end);
        m.AddLabel(body);
        var img = m.Load(tSrc, src);
        var max2 = m.CompositeConstruct(tI2, m.ISub(tI, w, i1), m.ISub(tI, h, i1));
        var p = m.CompositeConstruct(tI2, x, y);
        Instruction Tap(int dx, int dy)
        {
            var q = dx == 0 && dy == 0 ? p : m.GlslSClamp(tI2, m.IAdd(tI2, p, m.ConstantComposite(tI2, m.Constant(tI, dx), m.Constant(tI, dy))), z2, max2);
            return m.ImageFetch(tV4, img, q, ImageOperandsMask.Lod, i0);
        }
        var e = Tap(0, 0);
        var b = Tap(0, -1);
        var d = Tap(-1, 0);
        var f = Tap(1, 0);
        var hh = Tap(0, 1);
        var mn = m.GlslFMin(tV4, m.GlslFMin(tV4, m.GlslFMin(tV4, b, d), m.GlslFMin(tV4, f, hh)), e);
        var mx = m.GlslFMax(tV4, m.GlslFMax(tV4, m.GlslFMax(tV4, b, d), m.GlslFMax(tV4, f, hh)), e);
        var room = m.GlslFMin(tV4, mn, m.FSub(tV4, v1, mx));
        var amp = m.GlslSqrt(tV4, m.GlslFClamp(tV4, m.FDiv(tV4, room, m.FAdd(tV4, mx, vEps)), v0, v1));
        var wt = m.VectorTimesScalar(tV4, amp, peak);
        var sum = m.FAdd(tV4, m.FAdd(tV4, b, d), m.FAdd(tV4, f, hh));
        var num = m.FAdd(tV4, e, m.FMul(tV4, wt, sum));
        var den = m.FAdd(tV4, v1, m.VectorTimesScalar(tV4, wt, f4));
        var res = m.GlslFClamp(tV4, m.FDiv(tV4, num, den), v0, v1);
        var outv = m.CompositeInsert(tV4, m.CompositeExtract(tF, e, 3), res, 3);  // alpha unchanged
        m.ImageWrite(m.Load(tDst, dst), p, outv, ImageOperandsMask.MaskNone);
        m.Branch(end);
        m.AddLabel(end);
        m.Return();
        m.FunctionEnd();
        m.AddEntryPoint(ExecutionModel.GLCompute, main, "main", gid);
        m.AddExecutionMode(main, ExecutionMode.LocalSize, (LiteralInteger)8, (LiteralInteger)8, (LiteralInteger)1);
        return m.Generate();
    }
}
