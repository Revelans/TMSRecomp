// SMAA-style morphological anti-aliasing, three compute passes, built with Ryujinx's SPIR-V builder (Spv.Generator,
// MIT). Our own formulation of the published idea (Reshetov's MLAA / Jimenez et al.'s SMAA): no area or search
// textures, the coverage is computed in the shader.
//   pass 0 edges:   A = colour.  out.r = edge on the pixel's left side, out.g = edge on its top side (luma delta over
//                   the threshold and at least half the largest delta around it: local contrast adaptation)
//   pass 1 weights: A = edges.   For a top edge: walk left/right along the row to the segment ends (max steps, stop at
//                   crossing edges); each end's crossing edge says the silhouette steps up (+1/2) or down (-1/2) there;
//                   the line runs from each end's half step to 0 at the segment centre (Z, U and L shapes alike). The
//                   pixel's share of the area between line and edge: line above the edge -> the pixel above takes
//                   this pixel's colour (out.g), below -> this pixel takes the colour above (out.r). Left edges the
//                   same along the column (out.b: this pixel takes the left colour, out.a: the left pixel takes ours).
//   pass 2 blend:   A = colour, B = weights. P += wt (T - P) + wb (Bm - P) + wl (L - P) + wr (R - P), weights from
//                   this pixel (r, b), the pixel below (g) and right (a), scaled down when they sum over 1. Alpha kept.
//   pass 3: pass 2 into an R11G11B10 float image
//   set 0: binding 0 sampled image A, binding 1 sampled image B, binding 2 storage image out (rgba8)
//   push constants: int width, int height, float threshold, int max steps; local size 8 x 8
using System;
using Spv.Generator;
using static Spv.Specification;

static class Smaa
{
    public static byte[] Build(int pass)
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
        var tI2 = m.TypeVector(tI, 2);
        var tU3 = m.TypeVector(tU, 3);
        var tSrc = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 1, ImageFormat.Unknown);
        // pass 3 = pass 2 writing an R11G11B10 float image (the game's tone-mapped frame before FXAA is that format)
        var tDst = m.TypeImage(tF, Dim.Dim2D, 0, 0, 0, 2, pass == 3 ? ImageFormat.R11fG11fB10f : ImageFormat.Rgba8);
        if (pass == 3) m.AddCapability(Capability.StorageImageExtendedFormats);
        var pSrc = m.TypePointer(StorageClass.UniformConstant, tSrc);
        var pDst = m.TypePointer(StorageClass.UniformConstant, tDst);
        var tPc = m.TypeStruct(true, tI, tI, tF, tI);
        var pPc = m.TypePointer(StorageClass.PushConstant, tPc);
        var pPcI = m.TypePointer(StorageClass.PushConstant, tI);
        var pPcF = m.TypePointer(StorageClass.PushConstant, tF);
        var pIn = m.TypePointer(StorageClass.Input, tU3);
        var pFnI = m.TypePointer(StorageClass.Function, tI);
        var pFnV4 = m.TypePointer(StorageClass.Function, tV4);

        var srcA = m.Variable(pSrc, StorageClass.UniformConstant);
        var srcB = m.Variable(pSrc, StorageClass.UniformConstant);
        var dst = m.Variable(pDst, StorageClass.UniformConstant);
        var pc = m.Variable(pPc, StorageClass.PushConstant);
        var gid = m.Variable(pIn, StorageClass.Input);
        m.Decorate(srcA, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(srcA, Decoration.Binding, (LiteralInteger)0);
        m.Decorate(srcB, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(srcB, Decoration.Binding, (LiteralInteger)1);
        m.Decorate(dst, Decoration.DescriptorSet, (LiteralInteger)0);
        m.Decorate(dst, Decoration.Binding, (LiteralInteger)2);
        m.Decorate(dst, Decoration.NonReadable);
        m.Decorate(gid, Decoration.BuiltIn, (LiteralInteger)(int)BuiltIn.GlobalInvocationId);
        m.Decorate(tPc, Decoration.Block);
        for (int i = 0; i < 4; i++) m.MemberDecorate(tPc, i, Decoration.Offset, (LiteralInteger)(4 * i));
        foreach (var v in new[] { srcA, srcB, dst, pc, gid }) m.AddGlobalVariable(v);

        Instruction I(int v) => m.Constant(tI, v);
        Instruction F(float v) => m.Constant(tF, v);
        var f0 = F(0f);
        var v0 = m.ConstantComposite(tV4, f0, f0, f0, f0);
        var z2 = m.ConstantComposite(tI2, I(0), I(0));
        var luma = m.ConstantComposite(tV3, F(0.2126f), F(0.7152f), F(0.0722f));

        var main = m.Function(tVoid, FunctionControlMask.MaskNone, m.TypeFunction(tVoid, false));
        m.AddFunction(main);
        m.AddLabel(m.Label());
        // function variables first (SPIR-V: in the first block)
        var vRes = m.Variable(pFnV4, StorageClass.Function);
        var vA = m.Variable(pFnI, StorageClass.Function);
        var vK = m.Variable(pFnI, StorageClass.Function);
        var vB = m.Variable(pFnI, StorageClass.Function);
        var vK2 = m.Variable(pFnI, StorageClass.Function);
        foreach (var v in new[] { vRes, vA, vK, vB, vK2 }) m.AddLocalVariable(v);

        var w = m.Load(tI, m.AccessChain(pPcI, pc, I(0)));
        var h = m.Load(tI, m.AccessChain(pPcI, pc, I(1)));
        var thr = m.Load(tF, m.AccessChain(pPcF, pc, I(2)));
        var steps = m.Load(tI, m.AccessChain(pPcI, pc, I(3)));
        var id3 = m.Load(tU3, gid);
        var x = m.Bitcast(tI, m.CompositeExtract(tU, id3, 0));
        var y = m.Bitcast(tI, m.CompositeExtract(tU, id3, 1));
        var inside = m.LogicalAnd(tB, m.SLessThan(tB, x, w), m.SLessThan(tB, y, h));
        var body = m.Label();
        var end = m.Label();
        m.SelectionMerge(end, SelectionControlMask.MaskNone);
        m.BranchConditional(inside, body, end);
        m.AddLabel(body);
        var imgA = m.Load(tSrc, srcA);
        var max2 = m.CompositeConstruct(tI2, m.ISub(tI, w, I(1)), m.ISub(tI, h, I(1)));
        var p = m.CompositeConstruct(tI2, x, y);
        Instruction Fetch(Instruction img, Instruction qx, Instruction qy) =>
            m.ImageFetch(tV4, img, m.GlslSClamp(tI2, m.CompositeConstruct(tI2, qx, qy), z2, max2), ImageOperandsMask.Lod, I(0));
        Instruction Add(Instruction a, int d) => d == 0 ? a : m.IAdd(tI, a, I(d));
        Instruction Abs(Instruction a) => m.GlslFAbs(tF, a);
        Instruction Max(Instruction a, Instruction b) => m.GlslFMax(tF, a, b);
        void If(Instruction cond, Action then)
        {
            var t = m.Label();
            var e = m.Label();
            m.SelectionMerge(e, SelectionControlMask.MaskNone);
            m.BranchConditional(cond, t, e);
            m.AddLabel(t);
            then();
            m.Branch(e);
            m.AddLabel(e);
        }
        // while (cond()) step(): cond is straight-line code evaluated in the loop's check block
        void While(Func<Instruction> cond, Action step)
        {
            var header = m.Label();
            var check = m.Label();
            var loopBody = m.Label();
            var cont = m.Label();
            var merge = m.Label();
            m.Branch(header);
            m.AddLabel(header);
            m.LoopMerge(merge, cont, LoopControlMask.MaskNone);
            m.Branch(check);
            m.AddLabel(check);
            m.BranchConditional(cond(), loopBody, merge);
            m.AddLabel(loopBody);
            step();
            m.Branch(cont);
            m.AddLabel(cont);
            m.Branch(header);
            m.AddLabel(merge);
        }

        if (pass == 0)
        {
            Instruction L(int dx, int dy) { var f = Fetch(imgA, Add(x, dx), Add(y, dy)); return m.Dot(tF, m.VectorShuffle(tV3, f, f, 0, 1, 2), luma); }
            var c = L(0, 0);
            var l = L(-1, 0);
            var t = L(0, -1);
            var dl = m.Select(tF, m.SGreaterThan(tB, x, I(0)), Abs(m.FSub(tF, c, l)), f0);
            var dt = m.Select(tF, m.SGreaterThan(tB, y, I(0)), Abs(m.FSub(tF, c, t)), f0);
            var dr = Abs(m.FSub(tF, L(1, 0), c));
            var db = Abs(m.FSub(tF, L(0, 1), c));
            var dll = Abs(m.FSub(tF, l, L(-2, 0)));
            var dtt = Abs(m.FSub(tF, t, L(0, -2)));
            var mx = Max(Max(Max(dl, dt), Max(dr, db)), Max(dll, dtt));
            Instruction Edge(Instruction d) => m.Select(tF, m.LogicalAnd(tB, m.FOrdGreaterThan(tB, d, thr),
                                                                       m.FOrdGreaterThanEqual(tB, m.FMul(tF, d, F(2f)), mx)), F(1f), f0);
            m.Store(vRes, m.CompositeConstruct(tV4, Edge(dl), Edge(dt), f0, f0));
        }
        else if (pass == 1)
        {
            m.Store(vRes, v0);
            Instruction Top(Instruction qx, Instruction qy) => m.FOrdGreaterThan(tB, m.CompositeExtract(tF, Fetch(imgA, qx, qy), 1), F(0.5f));
            Instruction Left(Instruction qx, Instruction qy) => m.FOrdGreaterThan(tB, m.CompositeExtract(tF, Fetch(imgA, qx, qy), 0), F(0.5f));
            var e = Fetch(imgA, x, y);
            var half = F(0.5f);
            // one edge: run along axis u (the pixel's u = pu, other coordinate pv), 'has(u)' = edge continues at u,
            // 'crossNeg(u)' / 'crossPos(u)' = crossing edges at the boundary before u on the far / own side.
            // Writes the two weights (far side takes ours, we take the far side's) into res components ci_far, ci_own.
            void Segment(Instruction pu, Instruction limit, Func<Instruction, Instruction> has,
                         Func<Instruction, Instruction> crossFar, Func<Instruction, Instruction> crossOwn, int ciFar, int ciOwn)
            {
                // walk back
                m.Store(vA, pu);
                m.Store(vK, I(0));
                While(() =>
                {
                    var a = m.Load(tI, vA);
                    var ok = m.LogicalAnd(tB, m.SLessThan(tB, m.Load(tI, vK), steps), m.SGreaterThan(tB, a, I(0)));
                    var noCross = m.LogicalNot(tB, m.LogicalOr(tB, crossFar(a), crossOwn(a)));
                    return m.LogicalAnd(tB, m.LogicalAnd(tB, ok, noCross), has(m.ISub(tI, a, I(1))));
                }, () =>
                {
                    m.Store(vA, m.ISub(tI, m.Load(tI, vA), I(1)));
                    m.Store(vK, m.IAdd(tI, m.Load(tI, vK), I(1)));
                });
                // walk forward (b = last u with the edge; crossings at the boundary before b + 1)
                m.Store(vB, pu);
                m.Store(vK2, I(0));
                While(() =>
                {
                    var b = m.Load(tI, vB);
                    var b1 = m.IAdd(tI, b, I(1));
                    var ok = m.LogicalAnd(tB, m.SLessThan(tB, m.Load(tI, vK2), steps), m.SLessThan(tB, b, limit));
                    var noCross = m.LogicalNot(tB, m.LogicalOr(tB, crossFar(b1), crossOwn(b1)));
                    return m.LogicalAnd(tB, m.LogicalAnd(tB, ok, noCross), has(b1));
                }, () =>
                {
                    m.Store(vB, m.IAdd(tI, m.Load(tI, vB), I(1)));
                    m.Store(vK2, m.IAdd(tI, m.Load(tI, vK2), I(1)));
                });
                var a0 = m.Load(tI, vA);
                var b0 = m.Load(tI, vB);
                var bEnd = m.IAdd(tI, b0, I(1));
                // end heights: +1/2 toward the far side, -1/2 toward ours, 0 without a single crossing or at the step limit
                Instruction EndH(Instruction at, Instruction k)
                {
                    var far = crossFar(at);
                    var own = crossOwn(at);
                    var hv = m.Select(tF, m.LogicalAnd(tB, far, m.LogicalNot(tB, own)), half,
                                      m.Select(tF, m.LogicalAnd(tB, own, m.LogicalNot(tB, far)), F(-0.5f), f0));
                    return m.Select(tF, m.SLessThan(tB, k, steps), hv, f0);
                }
                var hA = EndH(a0, m.Load(tI, vK));
                var hB = EndH(bEnd, m.Load(tI, vK2));
                var fa = m.ConvertSToF(tF, a0);
                var fb = m.ConvertSToF(tF, bEnd);
                var len2 = m.FMul(tF, m.FSub(tF, fb, fa), half);  // half length
                var cen = m.FAdd(tF, fa, len2);
                var u0 = m.ConvertSToF(tF, pu);
                var u1 = m.FAdd(tF, u0, F(1f));
                // integral of a linear piece over [lo, hi] (0 when empty): (hi - lo) * (h(lo) + h(hi)) / 2
                Instruction Piece(Instruction lo, Instruction hi, Func<Instruction, Instruction> hAt)
                {
                    var len = m.GlslFMax(tF, m.FSub(tF, hi, lo), f0);
                    return m.FMul(tF, m.FMul(tF, len, half), m.FAdd(tF, hAt(lo), hAt(hi)));
                }
                var s1 = Piece(m.GlslFMax(tF, u0, fa), m.GlslFMin(tF, u1, cen), t => m.FDiv(tF, m.FMul(tF, hA, m.FSub(tF, cen, t)), len2));
                var s2 = Piece(m.GlslFMax(tF, u0, cen), m.GlslFMin(tF, u1, fb), t => m.FDiv(tF, m.FMul(tF, hB, m.FSub(tF, t, cen)), len2));
                var farW = m.FAdd(tF, Max(s1, f0), Max(s2, f0));
                var ownW = m.FAdd(tF, Max(m.FNegate(tF, s1), f0), Max(m.FNegate(tF, s2), f0));
                var r = m.Load(tV4, vRes);
                r = m.CompositeInsert(tV4, farW, r, ciFar);
                r = m.CompositeInsert(tV4, ownW, r, ciOwn);
                m.Store(vRes, r);
            }
            var ym1 = m.ISub(tI, y, I(1));
            var xm1 = m.ISub(tI, x, I(1));
            // top edge: along the row; far side = row y-1. crossing at boundary before u: left edges of (u, y-1) / (u, y)
            If(m.FOrdGreaterThan(tB, m.CompositeExtract(tF, e, 1), half), () =>
                Segment(x, m.ISub(tI, w, I(1)), u => Top(u, y), u => Left(u, ym1), u => Left(u, y), 1, 0));
            // left edge: along the column; far side = column x-1. crossing at boundary before v: top edges of (x-1, v) / (x, v)
            If(m.FOrdGreaterThan(tB, m.CompositeExtract(tF, e, 0), half), () =>
                Segment(y, m.ISub(tI, h, I(1)), v => Left(x, v), v => Top(xm1, v), v => Top(x, v), 3, 2));
        }
        else
        {
            var imgB = m.Load(tSrc, srcB);
            var P = Fetch(imgA, x, y);
            var wp = Fetch(imgB, x, y);
            var wt = m.CompositeExtract(tF, wp, 0);
            var wl = m.CompositeExtract(tF, wp, 2);
            var wb = m.Select(tF, m.SLessThan(tB, Add(y, 1), h), m.CompositeExtract(tF, Fetch(imgB, x, Add(y, 1)), 1), f0);
            var wr = m.Select(tF, m.SLessThan(tB, Add(x, 1), w), m.CompositeExtract(tF, Fetch(imgB, Add(x, 1), y), 3), f0);
            var sum = m.FAdd(tF, m.FAdd(tF, wt, wb), m.FAdd(tF, wl, wr));
            var sc = m.FDiv(tF, F(1f), Max(sum, F(1f)));
            Instruction Term(Instruction wgt, int dx, int dy) =>
                m.VectorTimesScalar(tV4, m.FSub(tV4, Fetch(imgA, Add(x, dx), Add(y, dy)), P), m.FMul(tF, wgt, sc));
            var o = m.FAdd(tV4, P, m.FAdd(tV4, m.FAdd(tV4, Term(wt, 0, -1), Term(wb, 0, 1)), m.FAdd(tV4, Term(wl, -1, 0), Term(wr, 1, 0))));
            m.Store(vRes, m.CompositeInsert(tV4, m.CompositeExtract(tF, P, 3), o, 3));  // alpha unchanged
        }
        m.ImageWrite(m.Load(tDst, dst), p, m.Load(tV4, vRes), ImageOperandsMask.MaskNone);
        m.Branch(end);
        m.AddLabel(end);
        m.Return();
        m.FunctionEnd();
        m.AddEntryPoint(ExecutionModel.GLCompute, main, "main", gid);
        m.AddExecutionMode(main, ExecutionMode.LocalSize, (LiteralInteger)8, (LiteralInteger)8, (LiteralInteger)1);
        return m.Generate();
    }
}
