// HDR output compute shader (setting hdr) for the runtime's present path, built with Ryujinx's SPIR-V builder
// (Spv.Generator, MIT) like Sharpen.cs. Input: the game's own final frame before its 8-bit copy (scene + UI in a float
// target, values gamma-encoded with 1/2.2 by the game; highlights keep values above 1 there, an SDR screen clips them).
//   set 0 binding 0: sampled image (that float frame), binding 1: storage image (output, R16G16B16A16_SFLOAT),
//   binding 2: storage buffer uint[] (subtitle bitmap, premultiplied RGBA8, R in the low byte, as Overlay.cs)
//   binding 3: sampled image (the 3D scene right after the game's FXAA draw, before its gamma pass and the UI; linear;
//   same size as binding 0; ignored when push constant scene = 0)
//   push constants: int src w, src h, dst w, dst h, subtitle x, y, w, h (w 0 = none); float paper white (nits),
//   knee (nits), peak (nits); int mode (0: HDR10 = BT.2020 + PQ, 1: scRGB = linear BT.709, 1.0 = 80 nits);
//   float itm (inverse tone mapping strength 0..1), float sat (extra saturation), int scene (binding 3 valid)
//   local size 8 x 8
// Per pixel: bilinear sample (any src -> dst size), subtitle over it (out = o + c (1 - o.a)), lin = c^2.2 (the 2.2
// display the game was made for). Scene mask (s121): where the final pixel equals the snapshot through the game's gamma
// (pow 1/2.2) no UI was drawn: w = 1 - smoothstep(0.02, 0.07, max |c - snap^(1/2.2)|), times (1 - subtitle alpha).
// Inverse tone mapping on scene pixels: luminance Y above 0.3 is lifted, x = (Y - 0.3) / 0.7 clamped, gain =
// 1 + (peak / paper - 1) * itm * w * x^2 (SDR white -> the peak; midtones almost unchanged; hue kept), then saturation
// around Y by 1 + sat * w. Then nits = lin * paper white, the brightest channel above the knee rolls off toward the
// peak (n' = k + (n - k) / (1 + (n - k) / (peak - k)), all channels scaled alike: no hue shift), then the encoding.
using System.Collections.Generic;
using Spv.Generator;
using static Spv.Specification;

static class Hdr
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
        var tV3 = m.TypeVector(tF, 3);
        var tV4 = m.TypeVector(tF, 4);
        var tB3 = m.TypeVector(tB, 3);
        var tI2 = m.TypeVector(tI, 2);
        var tU3 = m.TypeVector(tU, 3);
        var tM3 = m.TypeMatrix(tV3, 3);
        var tSrc = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 1, ImageFormat.Unknown);
        var tDst = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 2, ImageFormat.Rgba16f);
        var pSrc = m.TypePointer(StorageClass.UniformConstant, tSrc);
        var pDst = m.TypePointer(StorageClass.UniformConstant, tDst);
        var tArr = m.TypeRuntimeArray(tU);
        var tBuf = m.TypeStruct(true, tArr);
        var pBuf = m.TypePointer(StorageClass.StorageBuffer, tBuf);
        var pBufU = m.TypePointer(StorageClass.StorageBuffer, tU);
        var tPc = m.TypeStruct(true, tI, tI, tI, tI, tI, tI, tI, tI, tF, tF, tF, tI, tF, tF, tI);
        var pPc = m.TypePointer(StorageClass.PushConstant, tPc);
        var pPcI = m.TypePointer(StorageClass.PushConstant, tI);
        var pPcF = m.TypePointer(StorageClass.PushConstant, tF);
        var pIn = m.TypePointer(StorageClass.Input, tU3);

        var src = m.Variable(pSrc, StorageClass.UniformConstant);
        var scn = m.Variable(pSrc, StorageClass.UniformConstant);
        var dst = m.Variable(pDst, StorageClass.UniformConstant);
        var buf = m.Variable(pBuf, StorageClass.StorageBuffer);
        var pc = m.Variable(pPc, StorageClass.PushConstant);
        var gid = m.Variable(pIn, StorageClass.Input);
        m.Decorate(src, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(src, Decoration.Binding, (LiteralInteger)0);
        m.Decorate(scn, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(scn, Decoration.Binding, (LiteralInteger)3);
        m.Decorate(dst, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(dst, Decoration.Binding, (LiteralInteger)1);
        m.Decorate(dst, Decoration.NonReadable);
        m.Decorate(tArr, Decoration.ArrayStride, (LiteralInteger)4);
        m.Decorate(tBuf, Decoration.Block);
        m.MemberDecorate(tBuf, 0, Decoration.Offset, (LiteralInteger)0);
        m.Decorate(buf, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(buf, Decoration.Binding, (LiteralInteger)2);
        m.Decorate(buf, Decoration.NonWritable);
        m.Decorate(gid, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.GlobalInvocationId);
        m.Decorate(tPc, Decoration.Block);
        for (int k = 0; k < 15; k++) m.MemberDecorate(tPc, k, Decoration.Offset, (LiteralInteger)(4 * k));
        foreach (var v in new[] { src, scn, dst, buf, pc, gid }) m.AddGlobalVariable(v);

        var fc = new Dictionary<float, Instruction>();
        Instruction F(float x) => fc.TryGetValue(x, out var c) ? c : fc[x] = m.Constant(tF, x);
        var ic = new Dictionary<int, Instruction>();
        Instruction I(int x) => ic.TryGetValue(x, out var c) ? c : ic[x] = m.Constant(tI, x);
        Instruction V3(float x) => m.ConstantComposite(tV3, F(x), F(x), F(x));
        Instruction Add(Instruction a, Instruction b) => m.FAdd(tF, a, b);
        Instruction Sub(Instruction a, Instruction b) => m.FSub(tF, a, b);
        Instruction Mul(Instruction a, Instruction b) => m.FMul(tF, a, b);
        Instruction Div(Instruction a, Instruction b) => m.FDiv(tF, a, b);
        Instruction ToF(Instruction i) => m.ConvertSToF(tF, i);
        // BT.709 -> BT.2020 primaries (ITU-R BT.2087), columns
        var col0 = m.ConstantComposite(tV3, F(0.6274040f), F(0.0690970f), F(0.0163916f));
        var col1 = m.ConstantComposite(tV3, F(0.3292820f), F(0.9195400f), F(0.0880132f));
        var col2 = m.ConstantComposite(tV3, F(0.0433136f), F(0.0113612f), F(0.8955950f));
        var to2020 = m.ConstantComposite(tM3, col0, col1, col2);

        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        m.AddFunction(main);
        m.AddLabel(m.Label());
        Instruction Pc(int k) => m.Load(tI, m.AccessChain(pPcI, pc, I(k)));
        Instruction PcF(int k) => m.Load(tF, m.AccessChain(pPcF, pc, I(k)));
        var sw = Pc(0); var sh = Pc(1); var dw = Pc(2); var dh = Pc(3);
        var bx = Pc(4); var by = Pc(5); var bw = Pc(6); var bh = Pc(7);
        var paper = PcF(8); var knee = PcF(9); var peak = PcF(10); var mode = Pc(11);
        var itm = PcF(12); var sat = PcF(13); var hasScene = m.INotEqual(tB, Pc(14), I(0));
        var id3 = m.Load(tU3, gid);
        var x = m.Bitcast(tI, m.CompositeExtract(tU, id3, 0));
        var y = m.Bitcast(tI, m.CompositeExtract(tU, id3, 1));
        var inside = m.LogicalAnd(tB, m.SLessThan(tB, x, dw), m.SLessThan(tB, y, dh));
        var body = m.Label();
        var end = m.Label();
        m.SelectionMerge(end, SelectionControlMask.MaskNone);
        m.BranchConditional(inside, body, end);
        m.AddLabel(body);

        // bilinear sample of the game's frame
        var posx = Sub(Mul(Add(ToF(x), F(0.5f)), Div(ToF(sw), ToF(dw))), F(0.5f));
        var posy = Sub(Mul(Add(ToF(y), F(0.5f)), Div(ToF(sh), ToF(dh))), F(0.5f));
        var flx = m.GlslFloor(tF, posx);
        var fly = m.GlslFloor(tF, posy);
        var tx = Sub(posx, flx);
        var ty = Sub(posy, fly);
        var base2 = m.CompositeConstruct(tI2, m.ConvertFToS(tI, flx), m.ConvertFToS(tI, fly));
        var z2 = m.ConstantComposite(tI2, I(0), I(0));
        var max2 = m.CompositeConstruct(tI2, m.ISub(tI, sw, I(1)), m.ISub(tI, sh, I(1)));
        Instruction Bilinear(Instruction img) {
            Instruction Tap(int dx, int dy) {
                var q = m.GlslSClamp(tI2, m.IAdd(tI2, base2, m.ConstantComposite(tI2, I(dx), I(dy))), z2, max2);
                var t = m.ImageFetch(tV4, img, q, ImageOperandsMask.Lod, I(0));
                return m.VectorShuffle(tV3, t, t, 0, 1, 2);
            }
            var top = m.GlslFMix(tV3, Tap(0, 0), Tap(1, 0), m.CompositeConstruct(tV3, tx, tx, tx));
            var bot = m.GlslFMix(tV3, Tap(0, 1), Tap(1, 1), m.CompositeConstruct(tV3, tx, tx, tx));
            return m.GlslFMax(tV3, m.GlslFMix(tV3, top, bot, m.CompositeConstruct(tV3, ty, ty, ty)), V3(0f));
        }
        var c = Bilinear(m.Load(tSrc, src));
        // scene mask: 1 where no UI was drawn over the 3D scene
        var sg = m.GlslPow(tV3, m.GlslFMax(tV3, Bilinear(m.Load(tSrc, scn)), V3(1e-7f)), V3(1f / 2.2f));
        var dv = m.GlslFAbs(tV3, m.FSub(tV3, c, sg));
        var dmax = m.GlslFMax(tF, m.GlslFMax(tF, m.CompositeExtract(tF, dv, 0), m.CompositeExtract(tF, dv, 1)), m.CompositeExtract(tF, dv, 2));
        var wScene = m.Select(tF, hasScene, Sub(F(1f), m.GlslSmoothStep(tF, F(0.02f), F(0.07f), dmax)), F(0f));

        // subtitle bitmap over it (premultiplied); outside its rectangle o.a = 0
        var lx = m.ISub(tI, x, bx);
        var ly = m.ISub(tI, y, by);
        var inSub = m.LogicalAnd(tB, m.LogicalAnd(tB, m.SGreaterThanEqual(tB, lx, I(0)), m.SLessThan(tB, lx, bw)),
                                 m.LogicalAnd(tB, m.SGreaterThanEqual(tB, ly, I(0)), m.SLessThan(tB, ly, bh)));
        var idx = m.Select(tI, inSub, m.IAdd(tI, m.IMul(tI, ly, bw), lx), I(0));
        var word = m.Load(tU, m.AccessChain(pBufU, buf, I(0), idx));
        var o = m.GlslUnpackUnorm4x8(tV4, word);
        var oa = m.Select(tF, inSub, m.CompositeExtract(tF, o, 3), F(0f));
        var orgb = m.Select(tV3, m.CompositeConstruct(tB3, inSub, inSub, inSub),
                            m.VectorShuffle(tV3, o, o, 0, 1, 2), V3(0f));
        c = m.FAdd(tV3, orgb, m.VectorTimesScalar(tV3, c, Sub(F(1f), oa)));
        wScene = Mul(wScene, Sub(F(1f), oa));

        // nits, highlight roll-off on the brightest channel
        var lin = m.GlslPow(tV3, m.GlslFMax(tV3, c, V3(1e-7f)), V3(2.2f));
        // inverse tone mapping + saturation on scene pixels
        var lumw = m.ConstantComposite(tV3, F(0.2126f), F(0.7152f), F(0.0722f));
        var yl = m.Dot(tF, lin, lumw);
        var xr = m.GlslFClamp(tF, Div(Sub(yl, F(0.3f)), F(0.7f)), F(0f), F(1f));
        var gain = Add(F(1f), Mul(Mul(Mul(m.GlslFMax(tF, Sub(Div(peak, paper), F(1f)), F(0f)), itm), wScene), Mul(xr, xr)));
        lin = m.VectorTimesScalar(tV3, lin, gain);
        var y2 = m.Dot(tF, lin, lumw);
        var sk = Add(F(1f), Mul(sat, wScene));
        lin = m.GlslFMax(tV3, m.FAdd(tV3, m.CompositeConstruct(tV3, y2, y2, y2),
                                    m.VectorTimesScalar(tV3, m.FSub(tV3, lin, m.CompositeConstruct(tV3, y2, y2, y2)), sk)), V3(0f));
        var nits = m.VectorTimesScalar(tV3, lin, paper);
        var mx = m.GlslFMax(tF, m.GlslFMax(tF, m.CompositeExtract(tF, nits, 0), m.CompositeExtract(tF, nits, 1)), m.CompositeExtract(tF, nits, 2));
        var over = m.GlslFMax(tF, Sub(mx, knee), F(0f));
        var range = m.GlslFMax(tF, Sub(peak, knee), F(1f));
        var rolled = Add(knee, Div(over, Add(F(1f), Div(over, range))));
        var scale = m.Select(tF, m.FOrdGreaterThan(tB, mx, knee), Div(rolled, mx), F(1f));
        nits = m.VectorTimesScalar(tV3, nits, scale);

        // HDR10: BT.2020 primaries, SMPTE ST 2084 (PQ) of nits / 10000
        var n2020 = m.GlslFClamp(tV3, m.VectorTimesScalar(tV3, m.MatrixTimesVector(tV3, to2020, nits), F(1f / 10000)), V3(0f), V3(1f));
        var np = m.GlslPow(tV3, n2020, V3(0.1593017578125f));
        var pq = m.GlslPow(tV3, m.FDiv(tV3, m.FAdd(tV3, V3(0.8359375f), m.FMul(tV3, V3(18.8515625f), np)),
                                       m.FAdd(tV3, V3(1f), m.FMul(tV3, V3(18.6875f), np))), V3(78.84375f));
        // scRGB: linear BT.709, 1.0 = 80 nits
        var sc = m.VectorTimesScalar(tV3, nits, F(1f / 80));
        var isPq = m.IEqual(tB, mode, I(0));
        var res = m.Select(tV3, m.CompositeConstruct(tB3, isPq, isPq, isPq), pq, sc);

        var outv = m.CompositeConstruct(tV4, m.CompositeExtract(tF, res, 0), m.CompositeExtract(tF, res, 1), m.CompositeExtract(tF, res, 2), F(1f));
        m.ImageWrite(m.Load(tDst, dst), m.CompositeConstruct(tI2, x, y), outv, ImageOperandsMask.MaskNone);
        m.Branch(end);
        m.AddLabel(end);
        m.Return();
        m.FunctionEnd();
        m.AddEntryPoint(ExecutionModel.GLCompute, main, "main", gid);
        m.AddExecutionMode(main, ExecutionMode.LocalSize, (LiteralInteger)8, (LiteralInteger)8, (LiteralInteger)1);
        return m.Generate();
    }
}
