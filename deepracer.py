import math

def reward_function(params):

    waypoints = params['waypoints'] # waypoints mapeados de pistas em geral
    closest_waypoints = params['closest_waypoints'] # waypoint na frente e atrás do carro
    heading = params['heading'] # variação angular da posição do carro
    speed = params['speed'] # velocidade do carro
    off_track = params['is_offtrack'] # indica se o carro está dentro ou fora da pista
    


    reward = 1

    # Se saiu da pista haverá uma penalização severa
    if off_track == True:
        reward *= 0.5
    else:
    # Se está na pista haverá uma recompensa grande
        reward *= 200

    next_point = waypoints[closest_waypoints[1]] # frente do carro, são pontos que representam coordenadas
    prev_point = waypoints[closest_waypoints[0]] # atrás do carro, são pontos que representam coordenadas


    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) # conversão para radianos

    track_direction = math.degrees(track_direction) # conversão para graus

    MAX_INIT_CURV = 2
    MIN_LINE = 2.1
    MAX_LINE = 2.8

    # Saber a inclinação exata da pista
    absolute_value = abs(track_direction) # conversão para valor absoluto


    # Recompensa ou penalização baseado o quão a velocidade faz sentido para as curvas encontradas 
    # na pista

    # Se a curva ficar dentre este intervalo, então a velocidade não pode ultrapassar o limite estabelecido
    if 50 <= absolute_value <= 99 and speed > MAX_INIT_CURV:
        reward *= 0.5
    
    # Se a curva ficar dentre este intervalo, então a velocidade não pode ultrapassar o limite estabelecido
    if 0 <= absolute_value <= 20 and speed > MAX_LINE:
        reward *= 0.5
    # Se a velocidade se adequar a curva abaixo, que no caso seria quase uma linha reta devido
    # A baixa variação do absolute_value então, a velocidade poderá ser mais alta
    elif 0 <= absolute_value <= 20 and MIN_LINE <= speed <= MAX_LINE:
        reward *= 20 


    # variação entre a variação correta para um carro e a posição que o carro está
    direction_diff = abs(track_direction - heading) 
    # O track_direction pode variar de [-180, 180]
    # O heading pode variar de [-180, 180]
    
    # Normalização da variação para assumir intervalos dentre [0, 179]
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Recompensa se a variação para o eixo da pista em comparação com o eixo
    # do veiculo for pequena
    MAX_VARIATION = 10.0
    if direction_diff > MAX_VARIATION:
        reward *= 0.5

    return float(reward)