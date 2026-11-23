// Maxwell shader -> SPIR-V for the TMSRecomp runtime, over stdin/stdout.
//
// Request : u32 'NXSH', u32 stage (Ryujinx ShaderStage: 0 compute, 1 vertex, 2 tess ctrl, 3 tess eval, 4 geometry,
//           5 fragment), u32 length, [compute only: u32 local size x, y, z], u32 constants offset in the code, u32
//           constants size (cbuf 1; 0 = none), [vertex only: u8 x 32 attribute types (Ryujinx AttributeType: 0 float,
//           1 sint, 2 uint) per input location], code (graphics: starts at the 0x50-byte program header).
// Response: u32 status (0 ok), u32 code size used, u32 spirv length, spirv, u32 resource count, resources
//           {u8 kind (0 uniform, 1 storage, 2 texture, 3 image), u8 set, u16 binding, i32 slot, i32 handle,
//            i32 sampler type, i32 array length}, u32 fragment output map.
// Bindings: set 0, base + {uniform 0.., storage 32.., texture 64.., image 192..}; base = stage * 256, compute 6 * 256
// (binding 0 is Ryujinx's support buffer: render scales, viewport; the runtime binds it for every program).
using System;
using System.IO;
using Ryujinx.Common.Memory;
using Ryujinx.Graphics.Shader;
using Ryujinx.Graphics.Shader.Translation;

sealed class Accessor : IGpuAccessor
{
    readonly ulong[] _code;
    readonly int _base;
    readonly int[] _local;
    readonly byte[] _bytes;
    readonly int _cOff, _cSize;
    readonly byte[] _attrTypes;
    int _tex, _img;

    public Accessor(byte[] code, ShaderStage stage, int[] local, int cOff, int cSize, byte[] attrTypes)
    {
        _attrTypes = attrTypes;
        _local = local;
        _bytes = code;
        _cOff = cOff;
        _cSize = cSize;
        _code = new ulong[(code.Length + 7) / 8 + 64];
        Buffer.BlockCopy(code, 0, _code, 0, code.Length);
        _base = stage == ShaderStage.Compute ? 6 * 256 : (int)stage * 256;
    }

    public int QueryComputeLocalSizeX() => _local[0];
    public int QueryComputeLocalSizeY() => _local[1];
    public int QueryComputeLocalSizeZ() => _local[2];

    // Maxwell cbuf 1 = the shader's constant data (inside the code block); indirect branch tables live there
    public uint ConstantBuffer1Read(int offset) =>
        offset >= 0 && offset + 4 <= _cSize && _cOff + offset + 4 <= _bytes.Length ? BitConverter.ToUInt32(_bytes, _cOff + offset) : 0;

    // integer vertex formats (bone indices) need integer inputs: a float input fed from a UINT format is undefined in Vulkan
    public GpuGraphicsState QueryGraphicsState()
    {
        var types = new Array32<AttributeType>();
        for (int i = 0; i < 32 && _attrTypes != null; i++) types[i] = (AttributeType)_attrTypes[i];
        return new GpuGraphicsState(false, InputTopology.Points, false, TessPatchType.Triangles, TessSpacing.EqualSpacing,
            false, false, false, false, false, 1f, AlphaTestOp.Always, 0f, types, true, default, false, false, false, false);
    }

    public void Log(string message) => Console.Error.WriteLine("[shaderc] " + message);

    public ReadOnlySpan<ulong> GetCode(ulong address, int minimumSize)
    {
        int i = (int)(address / 8);
        return i < _code.Length ? new ReadOnlySpan<ulong>(_code, i, _code.Length - i) : ReadOnlySpan<ulong>.Empty;
    }

    public SetBindingPair CreateConstantBufferBinding(int index) => new(0, _base + index);
    public SetBindingPair CreateStorageBufferBinding(int index) => new(0, _base + 32 + index);
    public SetBindingPair CreateTextureBinding(int count, bool isBuffer) { int b = _base + 64 + _tex; _tex += count; return new(0, b); }
    public SetBindingPair CreateImageBinding(int count, bool isBuffer) { int b = _base + 192 + _img; _img += count; return new(0, b); }

    public int QuerySamplerArrayLengthFromPool() => 1;
    public int QueryTextureArrayLengthFromBuffer(int slot) => 1;
    public int QueryTextureArrayLengthFromPool() => 1;
    public void RegisterTexture(int handle, int cbufSlot) { }
}

static class Program
{
    static int Main()
    {
        var stdin = new BinaryReader(Console.OpenStandardInput());
        var stdout = new BinaryWriter(Console.OpenStandardOutput());
        for (;;)
        {
            uint magic;
            try { magic = stdin.ReadUInt32(); } catch (EndOfStreamException) { return 0; }
            if (magic != 0x4853584E) { Console.Error.WriteLine("[shaderc] bad magic"); return 1; }
            var stage = (ShaderStage)stdin.ReadUInt32();
            int len = stdin.ReadInt32();
            int[] local = stage == ShaderStage.Compute
                ? new[] { stdin.ReadInt32(), stdin.ReadInt32(), stdin.ReadInt32() }
                : new[] { 1, 1, 1 };
            int cOff = stdin.ReadInt32(), cSize = stdin.ReadInt32();
            byte[] attrTypes = stage == ShaderStage.Vertex ? stdin.ReadBytes(32) : null;
            byte[] code = stdin.ReadBytes(len);
            try
            {
                var acc = new Accessor(code, stage, local, cOff, cSize, attrTypes);
                var flags = stage == ShaderStage.Compute ? TranslationFlags.Compute : TranslationFlags.None;
                var ctx = Translator.CreateContext(0, acc, new TranslationOptions(TargetLanguage.Spirv, TargetApi.Vulkan, flags));
                ShaderProgram prog = ctx.Translate();
                string dumpDir = Environment.GetEnvironmentVariable("NXSHADER_DUMP_GLSL");
                if (dumpDir != null)
                {
                    // debug: the same shader as GLSL, readable (fresh context: a context translates once)
                    var gctx = Translator.CreateContext(0, new Accessor(code, stage, local, cOff, cSize, attrTypes), new TranslationOptions(TargetLanguage.Glsl, TargetApi.Vulkan, flags));
                    Directory.CreateDirectory(dumpDir);
                    string hash = Convert.ToHexString(System.Security.Cryptography.SHA1.HashData(code.AsSpan(0, Math.Min(code.Length, ctx.Size + 0x50)))).Substring(0, 12);
                    File.WriteAllText(Path.Combine(dumpDir, $"{stage}_{hash}.glsl"), gctx.Translate().Code);
                }
                var info = prog.Info;
                stdout.Write(0u);
                stdout.Write((uint)ctx.Size);
                stdout.Write((uint)prog.BinaryCode.Length);
                stdout.Write(prog.BinaryCode);
                stdout.Write((uint)(info.CBuffers.Count + info.SBuffers.Count + info.Textures.Count + info.Images.Count));
                foreach (var b in info.CBuffers) WriteRes(stdout, 0, b.Set, b.Binding, b.Slot, 0, 0, 1);
                foreach (var b in info.SBuffers) WriteRes(stdout, 1, b.Set, b.Binding, b.Slot, b.SbCbSlot | (b.SbCbOffset << 8), 0, 1);
                foreach (var t in info.Textures) WriteRes(stdout, 2, t.Set, t.Binding, t.CbufSlot, t.HandleIndex, (int)t.Type, t.ArrayLength);
                foreach (var t in info.Images) WriteRes(stdout, 3, t.Set, t.Binding, t.CbufSlot, t.HandleIndex, (int)t.Type, t.ArrayLength);
                stdout.Write((uint)info.FragmentOutputMap);
            }
            catch (Exception e)
            {
                Console.Error.WriteLine($"[shaderc] {stage} failed: {e.GetType().Name}: {e.Message}");
                stdout.Write(1u);
            }
            stdout.Flush();
        }
    }

    static void WriteRes(BinaryWriter w, byte kind, int set, int binding, int slot, int handle, int type, int count)
    {
        w.Write(kind);
        w.Write((byte)set);
        w.Write((ushort)binding);
        w.Write(slot);
        w.Write(handle);
        w.Write(type);
        w.Write(count);
    }
}
