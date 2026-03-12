# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:50:42 2026

@author: paulo.goncalves
"""

import random
import pygame
from pontos import ServicePoint


TIPOS_ATENDIMENTO = [
    ("Emergência obstétrica", 4),
    ("Violência doméstica", 3),
    ("Medicamento hormonal", 2),
    ("Pós-parto", 1),
]


REGIOES_ADMIN = [
    "Plano Piloto", "Ceilândia", "Taguatinga", "Samambaia", "Gama",
    "Santa Maria", "Park Way", "Lago Sul", "Lago Norte", "Sobradinho",
    "Sobradinho II", "Planaltina", "Paranoá", "São Sebastião",
    "Jardim Botânico", "Recanto das Emas", "Riacho Fundo", "Riacho Fundo II",
    "Vicente Pires", "Águas Claras", "SIA", "Cruzeiro", "Guará",
    "Núcleo Bandeirante", "Candangolândia", "Brazlândia", "Itapoã",
    "Varjão", "Arniqueira", "SCIA/Estrutural"
]


def load_and_scale_map(image_path: str, map_width: int, map_height: int) -> pygame.Surface:
    image = pygame.image.load(image_path)
    image = pygame.transform.smoothscale(image, (map_width, map_height))
    return image


def build_valid_positions(map_surface: pygame.Surface) -> list[tuple[int, int]]:
    valid_positions = []

    width = map_surface.get_width()
    height = map_surface.get_height()

    for x in range(width):
        for y in range(height):
            color = map_surface.get_at((x, y))

            r, g, b, *_ = color
            if not (r < 10 and g < 10 and b < 10):
                valid_positions.append((x, y))

    return valid_positions


def random_time_window(tipo_atendimento: str) -> tuple[int, int]:
    if tipo_atendimento == "Emergência obstétrica":
        return (0, 23)
    if tipo_atendimento == "Violência doméstica":
        return (6, 20)
    if tipo_atendimento == "Medicamento hormonal":
        return (8, 18)
    if tipo_atendimento == "Pós-parto":
        return (9, 17)
    return (8, 18)


def generate_service_points(valid_positions: list[tuple[int, int]], n_points: int) -> list[ServicePoint]:
    selected_positions = random.sample(valid_positions, n_points)
    points = []

    for i, (x, y) in enumerate(selected_positions, start=1):
        tipo_atendimento, prioridade = random.choice(TIPOS_ATENDIMENTO)
        tempo_inicio, tempo_fim = random_time_window(tipo_atendimento)

        point = ServicePoint(
            id=i,
            x=x,
            y=y,
            regiao_adm=random.choice(REGIOES_ADMIN),
            tipo_atendimento=tipo_atendimento,
            prioridade=prioridade,
            quantidade=random.randint(1, 5),
            tempo_inicio=tempo_inicio,
            tempo_fim=tempo_fim
        )
        points.append(point)

    return points


def create_initial_route(points: list[ServicePoint]) -> list[ServicePoint]:
    return sorted(points, key=lambda p: (-p.prioridade, p.tempo_inicio, p.id))