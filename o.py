import pygame
import numpy
from obj import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(1, 1, 1, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()

vertex_shader = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform mat4 theMatrix;
uniform vec3 lightpoint;

out vec2 vertexTexcoords;
out float intensity;
out vec3 mycolor;

void main() 
{
  intensity = dot(normal, normalize(lightpoint - position));
  gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
  mycolor = normal;
}
"""

shader1 = """
#version 460

layout (location = 0) out vec4 fragColor;

in float intensity;
void main()
{
  vec4 color;
  if(intensity<0.1){
    color= vec4(0,0,0,1);
  }
  else if(intensity>0.1 && intensity<0.2){
      color= vec4(1,1,1,1);
  }
  else if(intensity>0.6 && intensity<0.8){
      color= vec4(1,0,0,1);
  }
  else if(intensity>0.8 && intensity<1.6){
      color= vec4(0,0,0,1);
  }
    else if(intensity>1.6 && intensity<2.4){
      color= vec4(1,0,0,1);
  }
    else if(intensity>2.4 && intensity<3.2){
      color= vec4(1,1,1,1);
  }
    else if(intensity>3.2 && intensity<4){
      color= vec4(0,0,0,1);
  }
    
    else if(intensity>4.8 && intensity<5.6){
      color= vec4(1,0,0,1);
  }
    
    else if(intensity>5.6 && intensity<6.4){
      color= vec4(1,1,1,1);
  }
    
    else if(intensity>6.4 && intensity<7.2){
      color= vec4(0,0,0,1);
  }
      else if(intensity>7.2 && intensity<8){
      color= vec4(1,0,0,1);
  }
      else if(intensity>8 && intensity<8.8){
      color= vec4(1,0,0,1);
  }
      else if(intensity>8.8 && intensity<9.6){
      color= vec4(1,1,1,1);
  }
      else{
        color= vec4(1,0,0,1);
      }

    fragColor = color;

}

"""

shader2 = """
#version 460
layout(location = 0) out vec4 fragColor;

in vec3 mycolor;
in float intensity;

void main()
{
  if (mycolor.y + mycolor.x <0.1 ) {
    fragColor = vec4(1  ,0.9,0.8 , 1.0f);

  } else if(mycolor.y - mycolor.x > 0.1 && mycolor.y - mycolor.x < 0.2){
    fragColor = vec4(1 ,0.5 ,0.5 , 1.0f);
  }
  else if(mycolor.y + mycolor.x > 0.2 && mycolor.y + mycolor.x < 3){
    fragColor = vec4(0.43 ,0.25 * intensity,0.10, 1.0f);
  }
  else if(mycolor.y - mycolor.x > 0.3 && mycolor.y - mycolor.x < 4){
    fragColor = vec4(1  ,0.9,0.8 , 1.0f);
  }
  else if(mycolor.y + mycolor.x > 0.4 && mycolor.y + mycolor.x < 5){
    fragColor = vec4(1 ,0.5 ,0.5 , 1.0f);
  }
  else if(mycolor.y - mycolor.x > 0.5 && mycolor.y - mycolor.x < 6){
    fragColor = vec4(0.43 ,0.25 * intensity,0.10, 1.0f);
  }
  else if(mycolor.y + mycolor.x > 0.6 && mycolor.y + mycolor.x < 7){
    fragColor = vec4(1  ,0.9,0.8 , 1.0f);
  }
  else if(mycolor.y - mycolor.x > 0.7 && mycolor.y- mycolor.x < 8){
    fragColor = vec4(1 ,0.5 ,0.5 , 1.0f);
  }
  else if(mycolor.y + mycolor.x > 0.8 && mycolor.y + mycolor.x < 9){
    fragColor = vec4(0.43 ,0.25 * intensity,0.10, 1.0f);
  }
  else if(mycolor.y - mycolor.x > 0.9 && mycolor.y- mycolor.x < 1){
    fragColor = vec4(1  ,0.9,0.8 , 1.0f);
  }

}

"""
shader3="""
#version 460
layout(location = 0) out vec4 fragColor;

uniform int clock;
in vec3 mycolor;
in float intensity;



void main()
{
  if(mycolor.z < 0.33 && intensity < 0.5){
    fragColor = vec4(clock * 0.01f, 0,0, 1.0f);
  }
    else if(mycolor.z > 0.33 && mycolor.z < 0.66 && intensity < 0.5){
    fragColor = vec4(0, clock * 0.01f,0, 1.0f);
  }
    else if(mycolor.z > 0.66 && mycolor.z < 1 && intensity < 0.5){
    fragColor = vec4(0, 0,clock * 0.01f, 1.0f);
  }
  else{
    fragColor = vec4(1 - clock * 0.01f,1 -  clock * 0.01f,1 - clock * 0.01f, 1.0f);
  }
}

"""

cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(shader3, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)

mesh = Obj('./untitled.obj')

vertex_data = numpy.hstack((
  numpy.array(mesh.vertices, dtype=numpy.float32),
  numpy.array(mesh.normals, dtype=numpy.float32),
)).flatten()

index_data = numpy.array([[vertex[0] for vertex in face] for face in mesh.vfaces], dtype=numpy.uint32).flatten()

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(
  0, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)

element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(
  1, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(4 * 3)
)
glEnableVertexAttribArray(1)

glUseProgram(shader)


from math import sin

def render(up,down,side):
  i = glm.mat4(1)

  lightpoint = glm.vec3(up+20,side,down+10)

  translate = glm.translate(i, glm.vec3(0, 0, 0))
  rotate = glm.rotate(i, glm.radians(side), glm.vec3(0, 1, 0))
  scale = glm.scale(i, glm.vec3(5, 5, 5))

  model = translate * rotate * scale
  view = glm.lookAt(glm.vec3(0, up, down), glm.vec3(0, up, 0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), 1200/720, 0.1, 1000.0)

  theMatrix = projection * view * model

  glUniformMatrix4fv(
    glGetUniformLocation(shader, 'theMatrix'),
    1,
    GL_FALSE,
    glm.value_ptr(theMatrix)
  )
  glUniform3f(glGetUniformLocation(shader, "lightpoint"),
                        lightpoint.x, lightpoint.y, lightpoint.z)

glViewport(0, 0, 1200, 720)

a = 0
up = 0
down = 20
side = 0
running = True
render(up,down,side)
while running:
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  glUniform1i(
    glGetUniformLocation(shader, 'clock'),
    a
  )

  a += 1

  glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

  pygame.display.flip()
  clock.tick(15)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
            side -= 15
            render(up,down,side)
      elif event.key == pygame.K_d:
          side += 15
          render(up,down,side)
      elif event.key == pygame.K_w:
            up += 3
            render(up,down,side)
      elif event.key == pygame.K_s:
            up -= 3
            render(up,down,side)
      elif event.key == pygame.K_q:
            down += 5
            render(up,down,side)
      elif event.key == pygame.K_e:
            if(down > 5):
              down -= 5
              render(up,down,side)
            else:
                render(up,5,side)
      
            
