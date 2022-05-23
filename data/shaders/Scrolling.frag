#version 330 core
#define FRAG_COLOUR     0

in VertexData
{
    vec2    uvs;
    vec4    rgba;
} fs_in;

uniform vec3 rgb; // The inputed Values
uniform float time;
uniform int pressed;

uniform sampler2D image;
layout  (location = FRAG_COLOUR, index = 0) out vec4 fragColor;

void main()
{
    vec2 location = vec2(fs_in.uvs);
    float alpha = 1;
    vec3 scrollingColour = vec3(rgb.r, rgb.g, rgb.b);
    float before_time = time ;
    float timeBeg =  2;
    int key = pressed;

    // The 2 if statements determine if the right or left arrow in the shop has been clicked

     if (key == 2)
     {
        for (int i = 0; i < 9; ++i)
        {
            if (before_time > timeBeg)
            {
                timeBeg = timeBeg + 0.05; // this can be changed to make it smoother
                location.x = location.x  + 0.1; // This is moving the image of the sprite along the sprite back
            }
        }
    }

      if (key == 1)
     {
        for (int i = 0; i < 9; ++i)
        {
            if (before_time > timeBeg)
            {
                timeBeg = timeBeg + 0.05;
                location.x = location.x  - 0.1;
            }
        }
    }

    fragColor = vec4(scrollingColour, alpha) * texture(image, location);
}
