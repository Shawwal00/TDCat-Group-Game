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
    float alpha = 1;
    float amplitude = 0.01;
    float frequency = 2;
    vec3 lightColour = vec3(rgb.r, rgb.g, rgb.b);
    vec2 location = vec2(fs_in.uvs);
    float before_time = time - 1;
    float timeBeg =  0;
    while (before_time > timeBeg)
    {
        timeBeg = timeBeg + 0.1;// makes the light quicker/smoother
        // Create offset to wave the value normal to the movement
        float small_offset = (gl_FragCoord.x + (10 * sin(time + 1.5 * (gl_FragCoord.y * 0.02 + gl_FragCoord.x * 0.02))) - gl_FragCoord.y);
        // Moves the wave across the y = -x gradient
        float tempVal = abs(sin(time * frequency - (small_offset * amplitude)));

        if (tempVal > 0.95)
        {
            // Feathers the value to transition from 1,1,1 to 0.975,0.957, 0.975
            tempVal = 1 - 10 * (tempVal - 0.95)*(tempVal - 0.95);
            lightColour = vec3(tempVal, tempVal, tempVal);
        }
        else
        {
            lightColour = vec3(1, 1, 1);
            alpha = 1;
        }
        fragColor = vec4(lightColour, alpha) * texture(image, location);
    }
    fragColor = vec4(lightColour, alpha) * texture(image, location);
}
