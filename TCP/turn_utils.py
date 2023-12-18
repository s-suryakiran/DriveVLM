import carla
import numpy as np
import math

def maintain_speed(s,PREFERRED_SPEED,SPEED_THRESHOLD):
    ''' 
    this is a very simple function to maintan desired speed
    s arg is actual current speed
    '''
#     PREFERRED_SPEED = 30 # what it says
#     SPEED_THRESHOLD = 5 #defines when we get close to desired speed so we drop the
    
    throttle = 0
    
    if s >= PREFERRED_SPEED:
        throttle = 0
#         return 0
    elif s < PREFERRED_SPEED - SPEED_THRESHOLD:
        throttle = 0.8
#         return 0.8 # think of it as % of "full gas"
    else:
        throttle = 0.4
#         return 0.4 # tweak this if the car is way over or under preferred speed
    return throttle


import numpy as np

def normalize_vector(v):
    """ Normalize a 3D vector. """
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v

def slerp(v0, v1, t):
    """ Spherical linear interpolation between two vectors. """
    v0_normalized = normalize_vector(v0)
    v1_normalized = normalize_vector(v1)

    dot_product = np.dot(v0_normalized, v1_normalized)
    dot_product = np.clip(dot_product, -1.0, 1.0)

    theta = np.arccos(dot_product) * t
    sin_theta = np.sin(theta)

    s0 = np.cos(theta) - dot_product * sin_theta / np.sin(theta)
    s1 = sin_theta / np.sin(theta)

    return s0 * v0_normalized + s1 * v1_normalized

def rotate_vector(a, b, c, t1=0.8, t2=0.2):
    """ Rotate vector 'a' 80% towards 'b' and 20% towards 'c'. """
    # Normalize the vectors
    a_normalized = normalize_vector(a)
    b_normalized = normalize_vector(b)
    c_normalized = normalize_vector(c)

    # Spherical linear interpolation
    a_towards_b = slerp(a_normalized, b_normalized, t1)
    a_towards_c = slerp(a_normalized, c_normalized, t2)

    # Weighted combination of the two directions
    return a_towards_b * t1 + a_towards_c * t2

def give_output_vector(vector_a, vector_b, vector_c):

    # Example vectors
    vector_a = np.array([vector_a.x, vector_a.y, vector_a.z])
    vector_b = np.array([vector_b.x, vector_b.y, vector_b.z])
    vector_c = np.array([vector_c.x, vector_c.y, vector_c.z])

    # Rotate vector_a
    rotated_vector = rotate_vector(vector_a, vector_b, vector_c)
    rotated_vector_normalized = normalize_vector(rotated_vector)
    
    rotated_vector_normalized = carla.Vector3D(
                                                x= rotated_vector_normalized[0] ,
                                                y= rotated_vector_normalized[1] , 
                                                z= rotated_vector_normalized[2]  
                                            )


    return rotated_vector_normalized
    
def give_out_vector(waypoint, carpoint):
    
    return carla.Vector3D(
        x= waypoint.x - carpoint.x,
        y= waypoint.y - carpoint.y, 
        z= waypoint.z - carpoint.z 
    )

import sys
import math


def calculate_angle_between_vectors(vector_a, vector_b):
    # Calculate dot product
    dot_product = (vector_a.x * vector_b.x) + (vector_a.y * vector_b.y) + (vector_a.z * vector_b.z)

    # Calculate the magnitudes of the vectors
    magnitude_a = math.sqrt(vector_a.x**2 + vector_a.y**2 + vector_a.z**2)
    magnitude_b = math.sqrt(vector_b.x**2 + vector_b.y**2 + vector_b.z**2)

    # Calculate the cosine of the angle
    cos_angle = dot_product / ((magnitude_a * magnitude_b) + 1e-6)

    # Calculate the angle in radians and then convert to degrees
    angle = math.acos(cos_angle)  # Angle in radians
    
    cross_product = carla.Vector3D(
        x=vector_a.y * vector_b.z - vector_a.z * vector_b.y,
        y=vector_a.z * vector_b.x - vector_a.x * vector_b.z,
        z=vector_a.x * vector_b.y - vector_a.y * vector_b.x
    )
    
    direction = -1 if cross_product.z < 0 else 1
    
    return math.degrees(angle), direction # Convert to degrees


def average_vectors(vectors):
    avg_x = sum(vector.x for vector in vectors) / len(vectors)
    avg_y = sum(vector.y for vector in vectors) / len(vectors)
    avg_z = sum(vector.z for vector in vectors) / len(vectors)
    return carla.Vector3D(x=avg_x, y=avg_y, z=avg_z)


##################################################################
    
    
def return_closest_point_and_dist(waypoint_dict, vehicle):
    
    min_distance = float('inf')
    min_distance_point_index = float('inf')
    
    # Draw the route in the simulator
    for index in waypoint_dict.keys():
        cur_point_distance = (waypoint_dict[index]["point_object"][0].transform.location.x - vehicle.get_transform().location.x)**2 + (waypoint_dict[index]["point_object"][0].transform.location.z - vehicle.get_transform().location.z)**2 +(waypoint_dict[index]["point_object"][0].transform.location.y - vehicle.get_transform().location.y)**2   
        
        if cur_point_distance < min_distance:
            min_distance = cur_point_distance
            min_distance_point_index = index
            
    return min_distance, min_distance_point_index




class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def cross(self, other):
        return Vector3D(self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def perpendicular_distance_from_line_to_point(direction_vector, line_point, external_point):
    # Convert CARLA vectors to Vector3D
    line_vector = Vector3D(direction_vector.x, direction_vector.y, direction_vector.z)
    external_vector = Vector3D(external_point.x, external_point.y, external_point.z)
    line_point_vector = Vector3D(line_point.x, line_point.y, line_point.z)

    # Calculate the vector from the point on the line to the external point
    point_vector = external_vector - line_point_vector

    # Calculate the cross product and the norm
    cross_product = line_vector.cross(point_vector)
    distance = cross_product.norm() / line_vector.norm()

    return distance