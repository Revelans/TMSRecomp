// Edge-adaptive upscaling compute shader (setting upscaler = FSR 1) for the runtime's present path, built with
// Ryujinx's SPIR-V builder (Spv.Generator, MIT) like Sharpen.cs. Our own code for the idea of AMD FidelityFX Super
// Resolution 1's EASU pass (MIT): a 12-tap Lanczos-like kernel whose footprint is rotated along the local edge and
// stretched with the edge strength, then clamped to the 4 nearest pixels (no ringing). RCAS = our Sharpen pass after.
//   set 0 binding 0: sampled image (the game's frame), binding 1: storage image (the output, R8G8B8A8_UNORM)
//   push constants: int src width, src height, dst width, dst height; local size 8 x 8
// Per output pixel: p = (x + 0.5) * src / dst - 0.5, f = floor(p), t = p - f. Taps: the 2x2 pixels around p and the
// cross around them (12). Luma gradient g and edge strength r (|central difference| / (sum of the two one-sided
// differences): 1 on a ramp, 0 on a peak) at the 4 inner pixels, mixed bilinearly with t -> direction d (unit),
// strength s. Kernel per tap v = tap - t: u = (dot(v, d) * (1 + (k - 1) s), cross(v, d) * (1 - s / 2)), k = 1 /
// max(|d.x|, |d.y|); q = min(|u|^2, 1 / lobe), lobe = 0.5 - 0.29 s; w = (1.5625 (0.4 q - 1)^2 - 0.5625) (lobe q - 1)^2.
using System;
using System.Collections.Generic;
using Spv.Generator;
using static Spv.Specification;

static class Upscale
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
        var tPc = m.TypeStruct(true, tI, tI, tI, tI);
        var pPc = m.TypePointer(StorageClass.PushConstant, tPc);
        var pPcI = m.TypePointer(StorageClass.PushConstant, tI);
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
        for (int k = 0; k < 4; k++) m.MemberDecorate(tPc, k, Decoration.Offset, (LiteralInteger)(4 * k));
        foreach (var v in new[] { src, dst, pc, gid }) m.AddGlobalVariable(v);

        var fc = new Dictionary<float, Instruction>();
        Instruction F(float x) => fc.TryGetValue(x, out var c) ? c : fc[x] = m.Constant(tF, x);
        var ic = new Dictionary<int, Instruction>();
        Instruction I(int x) => ic.TryGetValue(x, out var c) ? c : ic[x] = m.Constant(tI, x);
        Instruction Add(Instruction a, Instruction b) => m.FAdd(tF, a, b);
        Instruction Sub(Instruction a, Instruction b) => m.FSub(tF, a, b);
        Instruction Mul(Instruction a, Instruction b) => m.FMul(tF, a, b);
        Instruction Abs(Instruction a) => m.GlslFAbs(tF, a);
        var z2 = m.ConstantComposite(tI2, I(0), I(0));
        var lumaW = m.ConstantComposite(tV4, F(0.299f), F(0.587f), F(0.114f), F(0f));

        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        m.AddFunction(main);
        m.AddLabel(m.Label());
        Instruction Pc(int k) => m.Load(tI, m.AccessChain(pPcI, pc, I(k)));
        var sw = Pc(0); var sh = Pc(1); var dw = Pc(2); var dh = Pc(3);
        var id3 = m.Load(tU3, gid);
        var x = m.Bitcast(tI, m.CompositeExtract(tU, id3, 0));
        var y = m.Bitcast(tI, m.CompositeExtract(tU, id3, 1));
        var inside = m.LogicalAnd(tB, m.SLessThan(tB, x, dw), m.SLessThan(tB, y, dh));
        var body = m.Label();
        var end = m.Label();
        m.SelectionMerge(end, SelectionControlMask.MaskNone);
        m.BranchConditional(inside, body, end);
        m.AddLabel(body);

        Instruction ToF(Instruction i) => m.ConvertSToF(tF, i);
        var posx = Sub(Mul(Add(ToF(x), F(0.5f)), m.FDiv(tF, ToF(sw), ToF(dw))), F(0.5f));
        var posy = Sub(Mul(Add(ToF(y), F(0.5f)), m.FDiv(tF, ToF(sh), ToF(dh))), F(0.5f));
        var flx = m.GlslFloor(tF, posx);
        var fly = m.GlslFloor(tF, posy);
        var tx = Sub(posx, flx);
        var ty = Sub(posy, fly);
        var base2 = m.CompositeConstruct(tI2, m.ConvertFToS(tI, flx), m.ConvertFToS(tI, fly));
        var max2 = m.CompositeConstruct(tI2, m.ISub(tI, sw, I(1)), m.ISub(tI, sh, I(1)));
        var img = m.Load(tSrc, src);

        // the 12 taps, by offset from the top-left inner pixel
        var taps = new (int dx, int dy)[] { (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2) };
        var col = new Dictionary<(int, int), Instruction>();
        var lum = new Dictionary<(int, int), Instruction>();
        foreach (var (dx, dy) in taps)
        {
            var q = m.GlslSClamp(tI2, m.IAdd(tI2, base2, m.ConstantComposite(tI2, I(dx), I(dy))), z2, max2);
            var c = m.ImageFetch(tV4, img, q, ImageOperandsMask.Lod, I(0));
            col[(dx, dy)] = c;
            lum[(dx, dy)] = m.Dot(tF, c, lumaW);
        }

        // direction + edge strength at the 4 inner pixels, mixed bilinearly
        Instruction Ratio(Instruction lo, Instruction mid, Instruction hi) =>
            m.FDiv(tF, Abs(Sub(hi, lo)), Add(Add(Abs(Sub(hi, mid)), Abs(Sub(mid, lo))), F(1f / 4096)));
        Instruction dirx = null, diry = null, len = null;
        foreach (var (a, b) in new[] { (0, 0), (1, 0), (0, 1), (1, 1) })
        {
            var wx = a == 0 ? Sub(F(1f), tx) : tx;
            var wy = b == 0 ? Sub(F(1f), ty) : ty;
            var w = Mul(wx, wy);
            var l = lum[(a, b)];
            var gx = Sub(lum[(a + 1, b)], lum[(a - 1, b)]);
            var gy = Sub(lum[(a, b + 1)], lum[(a, b - 1)]);
            var rx = Ratio(lum[(a - 1, b)], l, lum[(a + 1, b)]);
            var ry = Ratio(lum[(a, b - 1)], l, lum[(a, b + 1)]);
            var s = Mul(Add(Mul(rx, rx), Mul(ry, ry)), F(0.5f));
            dirx = dirx == null ? Mul(w, gx) : Add(dirx, Mul(w, gx));
            diry = diry == null ? Mul(w, gy) : Add(diry, Mul(w, gy));
            len = len == null ? Mul(w, s) : Add(len, Mul(w, s));
        }
        var d2 = Add(Mul(dirx, dirx), Mul(diry, diry));
        var flat = m.FOrdLessThan(tB, d2, F(1f / 32768));
        dirx = m.Select(tF, flat, F(1f), dirx);
        diry = m.Select(tF, flat, F(0f), diry);
        var inv = m.GlslInverseSqrt(tF, m.Select(tF, flat, F(1f), d2));
        dirx = Mul(dirx, inv);
        diry = Mul(diry, inv);
        var stretch = m.FDiv(tF, F(1f), m.GlslFMax(tF, Abs(dirx), Abs(diry)));
        var lx = Add(F(1f), Mul(Sub(stretch, F(1f)), len));
        var ly = Sub(F(1f), Mul(F(0.5f), len));
        var lobe = Sub(F(0.5f), Mul(F(0.29f), len));
        var clip = m.FDiv(tF, F(1f), lobe);

        Instruction acc = null, wsum = null;
        foreach (var (dx, dy) in taps)
        {
            var vx = Sub(F(dx), tx);
            var vy = Sub(F(dy), ty);
            var ux = Mul(Add(Mul(vx, dirx), Mul(vy, diry)), lx);
            var uy = Mul(Sub(Mul(vy, dirx), Mul(vx, diry)), ly);
            var q = m.GlslFMin(tF, Add(Mul(ux, ux), Mul(uy, uy)), clip);
            var wb = Sub(Mul(F(0.4f), q), F(1f));
            var wa = Sub(Mul(lobe, q), F(1f));
            var w = Mul(Sub(Mul(F(1.5625f), Mul(wb, wb)), F(0.5625f)), Mul(wa, wa));
            var cw = m.VectorTimesScalar(tV4, col[(dx, dy)], w);
            acc = acc == null ? cw : m.FAdd(tV4, acc, cw);
            wsum = wsum == null ? w : Add(wsum, w);
        }
        var res = m.VectorTimesScalar(tV4, acc, m.FDiv(tF, F(1f), wsum));
        var c00 = col[(0, 0)]; var c10 = col[(1, 0)]; var c01 = col[(0, 1)]; var c11 = col[(1, 1)];
        var mn = m.GlslFMin(tV4, m.GlslFMin(tV4, c00, c10), m.GlslFMin(tV4, c01, c11));
        var mx = m.GlslFMax(tV4, m.GlslFMax(tV4, c00, c10), m.GlslFMax(tV4, c01, c11));
        res = m.GlslFClamp(tV4, res, mn, mx);
        var outv = m.CompositeInsert(tV4, F(1f), res, 3);
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
