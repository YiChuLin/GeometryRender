#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

uniform mat4 projection;
uniform mat4 pose;

out vec3 FragPos;
out vec3 Pos;

void main(){
    FragPos = aNormal;
    Pos = aPos;
    //gl_Position = projection*view*vec4(aPos, 1.0);
    vec4 cam_space_position = pose*vec4(aPos, 1.0);
    cam_space_position.y = -cam_space_position.y;
    cam_space_position.z = -cam_space_position.z;
    gl_Position = projection*cam_space_position;
}
