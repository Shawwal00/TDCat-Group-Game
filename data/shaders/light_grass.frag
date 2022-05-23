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
    vec3 lightColour = vec3(rgb.r, rgb.g, rgb.b);
    vec2 location = vec2(fs_in.uvs);
    float screen_x = 1920 + 324;
    float lightOffsettEnd = 40;
    float lightOffsettStart = -40;
    float before_time = time - 1;
    float timeBeg =  1;

    while (before_time > timeBeg) //before_time is an inputed time varible
    //while timebeg is an int that increases this allows for the light to move across the screen
    {
        timeBeg = timeBeg + 0.1;// makes the light quicker/smoother

        lightOffsettStart = lightOffsettStart + 20;// Designates the starting for the light
        lightOffsettEnd = lightOffsettEnd + 20;

        if (gl_FragCoord.x < screen_x) // This insures that the parts not effected by the light will be normal
        {
            lightColour = vec3(1, 1, 1);
            alpha = 1;
            fragColor = vec4(lightColour, alpha) * texture(image, location);
        }
        //The 4 next if statements control the colour of the light and its alpha,each having slightly diffrent variables
        if (gl_FragCoord.x > screen_x - (lightOffsettEnd + gl_FragCoord.y * 0.3) && gl_FragCoord.x < screen_x -
        (lightOffsettStart + gl_FragCoord.y * 0.3))
        {
            lightColour = vec3(255,255,100) * 0.008;
            alpha = 0.7;
            fragColor = vec4(lightColour, alpha)  * texture(image, location);
            lightOffsettEnd = lightOffsettEnd - 5;
            lightOffsettStart = lightOffsettStart + 5;
        }
        if (gl_FragCoord.x > screen_x - (lightOffsettEnd + gl_FragCoord.y * 0.3) && gl_FragCoord.x < screen_x -
        (lightOffsettStart + gl_FragCoord.y * 0.3))
        {
            lightColour = vec3(255,255,150) * 0.008;
            alpha = 0.75;
            fragColor = vec4(lightColour, alpha)  * texture(image, location);
            lightOffsettEnd = lightOffsettEnd - 5;
            lightOffsettStart = lightOffsettStart + 5;
        }
        if (gl_FragCoord.x > screen_x - (lightOffsettEnd + gl_FragCoord.y * 0.3) && gl_FragCoord.x < screen_x
        - (lightOffsettStart + gl_FragCoord.y * 0.3))
        {
            lightColour = vec3(255,255,200) * 0.008;
            alpha = 0.8;
            fragColor = vec4(lightColour, alpha)  * texture(image, location);
            lightOffsettEnd = lightOffsettEnd - 5;
            lightOffsettStart = lightOffsettStart + 5;
        }
        if (gl_FragCoord.x > screen_x - (lightOffsettEnd + gl_FragCoord.y * 0.3) && gl_FragCoord.x < screen_x -
        (lightOffsettStart + gl_FragCoord.y * 0.3))
        {
            lightColour = vec3(255,255,255) * 0.008;
            alpha = 0.85;
            fragColor = vec4(lightColour, alpha);
            lightOffsettStart = lightOffsettStart + 5;
        }
    }
    fragColor = vec4(lightColour, alpha) * texture(image, location);
}
