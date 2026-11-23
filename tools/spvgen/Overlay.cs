// Subtitle overlay compute shader for the runtime's present path (tools/spvgen, Ryujinx's Spv.Generator, MIT):
// blends a premultiplied RGBA8 bitmap from a storage buffer over a rectangle of the frame in place.
//   set 0 binding 0: storage buffer uint[] (bitmap rows, R in the low byte), binding 1: storage image (the frame,
//   R8G8B8A8_UNORM, read + write)
//   push constants: int x, int y (rectangle origin in the frame), int width, int height (bitmap size)
//   local size 8 x 8; out.rgb = o.rgb + d.rgb * (1 - o.a), alpha unchanged
using Spv.Generator;
using static Spv.Specification;

static class Overlay
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
        var tArr = m.TypeRuntimeArray(tU);
        var tBuf = m.TypeStruct(true, tArr);
        var pBuf = m.TypePointer(StorageClass.StorageBuffer, tBuf);
        var pBufU = m.TypePointer(StorageClass.StorageBuffer, tU);
        var tDst = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 2, ImageFormat.Rgba8);
        var pDst = m.TypePointer(StorageClass.UniformConstant, tDst);
        var tPc = m.TypeStruct(true, tI, tI, tI, tI);
        var pPc = m.TypePointer(StorageClass.PushConstant, tPc);
        var pPcI = m.TypePointer(StorageClass.PushConstant, tI);
        var pIn = m.TypePointer(StorageClass.Input, tU3);

        var buf = m.Variable(pBuf, StorageClass.StorageBuffer);
        var dst = m.Variable(pDst, StorageClass.UniformConstant);
        var pc = m.Variable(pPc, StorageClass.PushConstant);
        var gid = m.Variable(pIn, StorageClass.Input);
        m.Decorate(tArr, Decoration.ArrayStride, (LiteralInteger)4);
        m.Decorate(tBuf, Decoration.Block);
        m.MemberDecorate(tBuf, 0, Decoration.Offset, (LiteralInteger)0);
        m.Decorate(buf, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(buf, Decoration.Binding, (LiteralInteger)0);
        m.Decorate(buf, Decoration.NonWritable);
        m.Decorate(dst, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(dst, Decoration.Binding, (LiteralInteger)1);
        m.Decorate(gid, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.GlobalInvocationId);
        m.Decorate(tPc, Decoration.Block);
        for (int i = 0; i < 4; i++) m.MemberDecorate(tPc, i, Decoration.Offset, (LiteralInteger)(4 * i));
        foreach (var v in new[] { buf, dst, pc, gid }) m.AddGlobalVariable(v);

        var i0 = m.Constant(tI, 0);
        var f1 = m.Constant(tF, 1f);

        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        m.AddFunction(main);
        m.AddLabel(m.Label());
        Instruction Pc(int i) => m.Load(tI, m.AccessChain(pPcI, pc, m.Constant(tI, i)));
        var ox = Pc(0);
        var oy = Pc(1);
        var w = Pc(2);
        var h = Pc(3);
        var id3 = m.Load(tU3, gid);
        var x = m.Bitcast(tI, m.CompositeExtract(tU, id3, 0));
        var y = m.Bitcast(tI, m.CompositeExtract(tU, id3, 1));
        var inside = m.LogicalAnd(tB, m.SLessThan(tB, x, w), m.SLessThan(tB, y, h));
        var body = m.Label();
        var end = m.Label();
        m.SelectionMerge(end, SelectionControlMask.MaskNone);
        m.BranchConditional(inside, body, end);
        m.AddLabel(body);
        var word = m.Load(tU, m.AccessChain(pBufU, buf, i0, m.IAdd(tI, m.IMul(tI, y, w), x)));
        var o = m.GlslUnpackUnorm4x8(tV4, word);
        var a = m.CompositeExtract(tF, o, 3);
        var visible = m.FOrdGreaterThan(tB, a, m.Constant(tF, 0f));  // fully transparent texels leave the frame alone
        var blend = m.Label();
        var blendEnd = m.Label();
        m.SelectionMerge(blendEnd, SelectionControlMask.MaskNone);  // must come right before its branch
        m.BranchConditional(visible, blend, blendEnd);
        m.AddLabel(blend);
        var img = m.Load(tDst, dst);
        var p = m.CompositeConstruct(tI2, m.IAdd(tI, ox, x), m.IAdd(tI, oy, y));
        var d = m.ImageRead(tV4, img, p, ImageOperandsMask.MaskNone);
        var res = m.FAdd(tV4, o, m.VectorTimesScalar(tV4, d, m.FSub(tF, f1, a)));
        var outv = m.CompositeInsert(tV4, m.CompositeExtract(tF, d, 3), res, 3);
        m.ImageWrite(img, p, outv, ImageOperandsMask.MaskNone);
        m.Branch(blendEnd);
        m.AddLabel(blendEnd);
        m.Branch(end);
        m.AddLabel(end);
        m.Return();
        m.FunctionEnd();
        m.AddEntryPoint(ExecutionModel.GLCompute, main, "main", gid);
        m.AddExecutionMode(main, ExecutionMode.LocalSize, (LiteralInteger)8, (LiteralInteger)8, (LiteralInteger)1);
        return m.Generate();
    }
}
