#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

uniform mat4 projection;
uniform mat3 rotation;
uniform mat3 K;
uniform vec3 origin;

out vec3 FragPos;
out vec3 Pos;

void main(){
    FragPos = aNormal;
    Pos = aPos;
    //gl_Position = projection*view*vec4(aPos, 1.0);
    vec3 dw = aPos - origin;
    vec3 d = rotation*dw;
    vec3 d_pix = K*d;//vec3(d.x/d.z, d.y, 1.0);
    vec4 unprojected_point = vec4(d_pix, 1.0);
    gl_Position = projection*unprojected_point;
}
