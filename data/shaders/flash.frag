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
    vec3 firstColour = vec3(rgb.r, rgb.g, rgb.b); // Is taking in the colour
    float alpha = 1;
        if (time >  0.2) // Time variable
        {
            alpha = 0.8; // This determines how visible the the object is
        }
        if (time > 0.4)
        {
            alpha = 0.7;
        }
        if (time > 0.5)
        {
            alpha = 0.6;
        }
    fragColor = vec4(firstColour, alpha) * texture(image, fs_in.uvs);
}
