#version 330 core

in vec3 Normal;
in vec3 Pos;

uniform int operationCode;

out vec4 FragColor;

void main()
{
  if(operationCode == 0){
    vec3 normalColor = (Normal + 1.0)/2.0;
    FragColor = vec4(normalColor, 1.0);
  }else if(operationCode == 1){
    // Pos x : -0.05 ~ 0.02
    // Pos y : -0.2 ~ 0.1
    // Pos z : -0.75 ~ -0.6
    vec3 scaled_pos = vec3(1.0, 1.0, 1.0);
    scaled_pos.x = (Pos.x + 0.05) / (0.02 + 0.05);
    scaled_pos.y = (Pos.y + 0.2) / (0.1 + 0.2);
    scaled_pos.z = (Pos.z + 0.75) / (-0.6 + 0.75);
    vec3 posColor = scaled_pos;
    FragColor = vec4(posColor, 1.0);
  }else{
    FragColor = vec4(1.0, 1.0, 1.0, 1.0);
  }

  //float normalized_z = (position.y+1.0)/2.0;
  //vec3 positionColor = (Pos + 1.0)/2.0;
  //FragColor = vec4(positionColor, 1.0);
}
