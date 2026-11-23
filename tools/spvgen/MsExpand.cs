// MSAA expand shaders: draw a single-sample image into its multisampled twin (the runtime's MSAA, vk_replay.cpp
// MsTwin) with one full-screen triangle, so every sample of each pixel gets the pixel's colour. Built with Ryujinx's
// SPIR-V builder (Spv.Generator, MIT).
//   msxv (vertex): positions from gl_VertexIndex 0..2 = (-1,-1) (3,-1) (-1,3)
//   msxf (fragment): out0 = texelFetch(set 0 binding 0, ivec2(gl_FragCoord.xy), 0)
using Spv.Generator;
using static Spv.Specification;

static class MsExpand
{
    public static byte[] Build(bool vertex)
    {
        var m = new Module(0x00010300);
        m.AddCapability(Capability.Shader);
        m.SetMemoryModel(AddressingModel.Logical, MemoryModel.GLSL450);
        var tVoid = m.TypeVoid();
        var tF = m.TypeFloat(32);
        var tI = m.TypeInt(32, 1);
        var tV2 = m.TypeVector(tF, 2);
        var tV4 = m.TypeVector(tF, 4);
        var tI2 = m.TypeVector(tI, 2);
        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        if (vertex)
        {
            var pInI = m.TypePointer(StorageClass.Input, tI);
            var pOut = m.TypePointer(StorageClass.Output, tV4);
            var vid = m.Variable(pInI, StorageClass.Input);
            var pos = m.Variable(pOut, StorageClass.Output);
            m.Decorate(vid, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.VertexIndex);
            m.Decorate(pos, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.Position);
            m.AddGlobalVariable(vid);
            m.AddGlobalVariable(pos);
            m.AddFunction(main);
            m.AddLabel(m.Label());
            var i = m.Load(tI, vid);
            // x = (i == 1) ? 3 : -1, y = (i == 2) ? 3 : -1
            var bT = m.TypeBool();
            var three = m.Constant(tF, 3f);
            var neg = m.Constant(tF, -1f);
            var x = m.Select(tF, m.IEqual(bT, i, m.Constant(tI, 1)), three, neg);
            var y = m.Select(tF, m.IEqual(bT, i, m.Constant(tI, 2)), three, neg);
            m.Store(pos, m.CompositeConstruct(tV4, x, y, m.Constant(tF, 0f), m.Constant(tF, 1f)));
            m.Return();
            m.FunctionEnd();
            m.AddEntryPoint(ExecutionModel.Vertex, main, "main", vid, pos);
        }
        else
        {
            var tSrc = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 1, ImageFormat.Unknown);
            var pSrc = m.TypePointer(StorageClass.UniformConstant, tSrc);
            var pIn = m.TypePointer(StorageClass.Input, tV4);
            var pOut = m.TypePointer(StorageClass.Output, tV4);
            var src = m.Variable(pSrc, StorageClass.UniformConstant);
            var fc = m.Variable(pIn, StorageClass.Input);
            var o = m.Variable(pOut, StorageClass.Output);
            m.Decorate(src, Decoration.DescriptorSet, (LiteralInteger)0);
            m.Decorate(src, Decoration.Binding, (LiteralInteger)0);
            m.Decorate(fc, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.FragCoord);
            m.Decorate(o, Decoration.Location, (LiteralInteger)0);
            foreach (var v in new[] { src, fc, o }) m.AddGlobalVariable(v);
            m.AddFunction(main);
            m.AddLabel(m.Label());
            var f = m.Load(tV4, fc);
            var xy = m.ConvertFToS(tI2, m.VectorShuffle(tV2, f, f, 0, 1));
            m.Store(o, m.ImageFetch(tV4, m.Load(tSrc, src), xy, ImageOperandsMask.Lod, m.Constant(tI, 0)));
            m.Return();
            m.FunctionEnd();
            m.AddEntryPoint(ExecutionModel.Fragment, main, "main", fc, o);
            m.AddExecutionMode(main, ExecutionMode.OriginUpperLeft);
        }
        return m.Generate();
    }
}
