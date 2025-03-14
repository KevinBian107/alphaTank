import pygame
import random
import math
from env.config import *

def reflect_vector(incident, normal):
    """计算反弹方向：反射向量 = incident - 2 * (incident ⋅ normal) * normal"""
    incident_vec = pygame.Vector2(incident)
    normal_vec = pygame.Vector2(normal).normalize()
    reflection = incident_vec - 2 * incident_vec.dot(normal_vec) * normal_vec
    return reflection

# OBB vs AABB 碰撞检测（分离轴定理 SAT）
def project_polygon(corners, axis):
    """计算多边形在轴上的投影"""
    dots = [corner.dot(axis) for corner in corners]
    return min(dots), max(dots)

def is_separating_axis(axis, corners1, corners2):
    """判断某轴是否是分离轴"""
    min1, max1 = project_polygon(corners1, axis)
    min2, max2 = project_polygon(corners2, axis)
    return max1 < min2 - EPSILON or max2 < min1 - EPSILON  # 修正误差

def obb_vs_aabb(obb_corners, aabb_rect):
    """检测 OBB vs AABB 碰撞"""
    aabb_corners = [
        pygame.Vector2(aabb_rect.topleft),
        pygame.Vector2(aabb_rect.topright),
        pygame.Vector2(aabb_rect.bottomright),
        pygame.Vector2(aabb_rect.bottomleft)
    ]

    # 计算 OBB 的法向量（旋转矩形的边）
    obb_axes = [
        (obb_corners[1] - obb_corners[0]).normalize(),
        (obb_corners[3] - obb_corners[0]).normalize()
    ]

    # AABB 的法向量（固定的 x/y 轴）
    aabb_axes = [pygame.Vector2(1, 0), pygame.Vector2(0, 1)]

    # 检测所有轴
    for axis in obb_axes + aabb_axes:
        if is_separating_axis(axis, obb_corners, aabb_corners):
            return False  # 存在分离轴，无碰撞
    return True  # 所有轴都重叠，有碰撞

def angle_to_vector(angle, speed, r=1):
    """将角度拆分为 dx, dy 两个分量"""
    angle_rad = math.radians(angle)  # 角度转换为弧度
    dx = speed * r * math.cos(angle_rad)
    dy = speed * r * math.sin(angle_rad)
    return dx, dy

def corner_to_xy(tank):
    corner1,corner2,corner3,corner4 = tank.get_corners()
    return float(corner1.x), float(corner1.y), float(corner2.x), float(corner2.y), float(corner3.x), float(corner3.y), float(corner4.x), float(corner4.y)

def euclidean_distance(cell_a, cell_b):
    (r1, c1) = cell_a
    (r2, c2) = cell_b
    return math.sqrt((r1 - r2) ** 2 + (c1 - c2) ** 2)