#version 330 core

in vec3 FragPos;
in vec3 Pos;

out vec4 FragColor;

void main()
{
  vec3 normalColor = (FragPos + 1.0)/2.0;
  FragColor = vec4(normalColor, 1.0);
  //float normalized_z = (position.y+1.0)/2.0;
  //vec3 positionColor = (Pos + 1.0)/2.0;
  //FragColor = vec4(positionColor, 1.0);
}
