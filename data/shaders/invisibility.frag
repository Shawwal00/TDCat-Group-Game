#version 330 core
#define FRAG_COLOUR     0

in VertexData
{
    vec2    uvs;
    vec4    rgba;
} fs_in;

uniform vec3 rgb; // The inputed Values
uniform float time;

uniform sampler2D image;
layout  (location = FRAG_COLOUR, index = 0) out vec4 fragColor;

void main()
{
    vec3 firstColour = vec3(rgb.r, rgb.g, rgb.b);
    float frequency = 10;
    float alpha = sin(time * frequency) * 0.3 + 0.3;
    fragColor = vec4(firstColour, alpha) * texture(image, fs_in.uvs);
}

