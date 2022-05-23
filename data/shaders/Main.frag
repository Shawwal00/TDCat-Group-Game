#version 330 core
#define FRAG_COLOUR     0

in VertexData
{
    vec2    uvs;
    vec4    rgba;
} fs_in;

uniform vec3 rgb;
uniform sampler2D image;
uniform float alpha;
layout  (location = FRAG_COLOUR, index = 0) out vec4 fragColor;

// This shader is the main base shader that is always used
void main()
{
    fragColor = vec4(rgb, fs_in.rgba.a * alpha) * texture(image, fs_in.uvs);
}
