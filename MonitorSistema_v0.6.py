# -*- coding: utf-8 -*-
"""
Created on Mon Jan  11 22:00:19 2018
@author: Alexander.Silva
"""
import pygame, psutil, cpuinfo, os, time, datetime

pygame.init()
# Cores:
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
azul = (0,0,255)
vermelho = (255,0,0)   
# Iniciando a janela principal
larguraTela = 800
alturaTela = 600
tela = pygame.display.set_mode((larguraTela, alturaTela))
pygame.display.set_caption("Monitor de Sistema")
pygame.display.init()   
# Superfícies para mostrar as informações:
s0 = pygame.surface.Surface((larguraTela, alturaTela/6))
s1 = pygame.surface.Surface((larguraTela, alturaTela/6))
s2 = pygame.surface.Surface((larguraTela, alturaTela/6))
s3 = pygame.surface.Surface((larguraTela, alturaTela/6))
s4 = pygame.surface.Surface((larguraTela, alturaTela/6))
s5 = pygame.surface.Surface((larguraTela, alturaTela/6))
# Inicializa fonte do sistema
pygame.font.init()
font = pygame.font.Font(None, 22)
# Cria relógio
clock = pygame.time.Clock()
# Contador de tempo
cont = 60
# Obtém informações da CPU
infoCpu = cpuinfo.get_cpu_info()
# Retorna uma lista de percentual de uso de cada CPU:
listCpuPercent = psutil.cpu_percent(interval=1, percpu=True)   

# Mostra as informações de CPU escolhidas:
def mostraInfoCpu():
    s0.fill(branco)
    mostraTexto(s0, "Nome:", "brand", 3)
    mostraTexto(s0, "Arquitetura:", "arch", 23)
    mostraTexto(s0, "Palavra (bits):", "bits", 43)
    mostraTexto(s0, "Frequência (MHz):", "freq", 63)
    mostraTexto(s0, "Núcleos (físicos):", "nucleos", 83)
    tela.blit(s0, (0, 0))
        
# Mostra texto de acordo com uma chave:
def mostraTexto(s0, nome, chave, pos_y):
    text = font.render(nome, True, preto)
    s0.blit(text, (10, pos_y))
    if chave == "freq":
        s1 = str(round(psutil.cpu_freq().current, 2))
    elif chave == "nucleos":
        s1 = str(psutil.cpu_count())
        s1 = s1 + " (" + str(psutil.cpu_count(logical=True)) + ")"
    else:
        s1 = str(infoCpu[chave])
    text = font.render(s1, True, cinza)
    s0.blit(text, (160, pos_y))

# Mostra o percentual de uso de CPU:
def mostraUsoCpu(s1, listCpuPercent):
    s1.fill(cinza)
    numCpu = len(listCpuPercent)
    x = y = 10
    desl = 10
    alt = s0.get_height()-2*y
    larg = (s0.get_width()-2*x - (numCpu+1)*desl)/numCpu
    d = x + desl
    for i in listCpuPercent:
        pygame.draw.rect(s0, vermelho, (d, y, larg, alt))
        pygame.draw.rect(s0, azul, (d, y, larg, (1-i/100)*alt))
        d = d + larg + desl       
        tela.blit(s0, (0, alturaTela/6))
    textoCpu1 = font.render('Core 1: ' + str(listCpuPercent[0]) + ' %', 1, branco)
    tela.blit(textoCpu1,(60, alturaTela/6 + 50))
    textoCpu2 = font.render('Core 2: ' + str(listCpuPercent[1]) + ' %', 1, branco)
    tela.blit(textoCpu2,(260, alturaTela/6 + 50))
    textoCpu3 = font.render('Core 3: ' + str(listCpuPercent[2]) + ' %', 1, branco)
    tela.blit(textoCpu3,(440, alturaTela/6 + 50))
    textoCpu4 = font.render('Core 4: ' + str(listCpuPercent[3]) + ' %', 1, branco)
    tela.blit(textoCpu4,(640, alturaTela/6 + 50))

# Mostra a capacidade de MP em uso e total:       
def mostraUsoMemoria():    
    mem = psutil.virtual_memory()
    largBarraMem = larguraTela-2*20
    s2.fill(cinza)
    pygame.draw.rect(s2, azul, (20,30,largBarraMem,50))
    tela.blit(s2, (0,2*alturaTela/6))
    largBarraMem = largBarraMem*mem.percent/100
    pygame.draw.rect(s2, vermelho, (20,30,largBarraMem,50))
    tela.blit(s2,(0,2*alturaTela/6))
    total = round(mem.total/(1024*1024*1024),2)
    totalEmUso = round(mem.used/(1024*1024*1024),2)
    textoMemTopo = font.render('Capacidade total MP: ' 
                               + str(total) + ' GB', 1, branco)
    textoBarra = font.render(str(totalEmUso) + ' GB', 1, branco)
    tela.blit(textoMemTopo,(20,2*alturaTela/6 + 10))
    tela.blit(textoBarra,(250,300))

# Mostra a capacidade do disco rígido em uso e total:
def mostraUsoDisco():
    lista_info_particao = psutil.disk_partitions()
    disco = psutil.disk_usage('.')
    largBarraDisco = larguraTela-2*20
    s3.fill(cinza)
    pygame.draw.rect(s3, azul, (20,30,largBarraDisco,50))
    tela.blit(s3, (0,3*alturaTela/6))
    largBarraDisco = largBarraDisco*disco.percent/100
    pygame.draw.rect(s3, vermelho, (20,30,largBarraDisco,50))
    tela.blit(s3,(0,3*alturaTela/6))
    total = round(disco.total/(1024*1024*1024),2)
    discoUso = round(disco.used/(1024*1024*1024),2)
    textoDiscoTopo = font.render('Capacidade total Disco Rígido: ' 
                                 + str(total) + ' GB', 1, branco)
    textoBarra = font.render(str(discoUso) + ' GB', 1, branco)
    textoInfoParticao = font.render('| Dispositivo: ' + str(lista_info_particao[0].device)
                                    + '  |  Sistema de Arquivo: '
                                    + str(lista_info_particao[0].fstype), 1, branco)
    tela.blit(textoInfoParticao, (350, 3*alturaTela/6 + 10))
    tela.blit(textoDiscoTopo,(20, 3*alturaTela/6 + 10))
    tela.blit(textoBarra,(25, 3*alturaTela/6 + 50))

# Mostra o ip da interface de rede local:
def mostraIp():
    dicIpAdress = psutil.net_if_addrs()
    s4.fill(branco)
    tela.blit(s4,(0, 4*alturaTela/6))
    textoIpAdress = font.render('Rede local Ip: ' 
                                + dicIpAdress['enp0s7'][0].address, 1, preto)
    tela.blit(textoIpAdress,(20, 410))

def mostraInfoDir():
    #s4.fill(branco)
    #tela.blit(s4, (0, 4*alturaTela/5))

    lista = os.listdir()
    dic = {}

    for i in lista:
        if os.path.isfile(i):
            dic[i] = []
            dic[i].append(os.stat(i).st_size)
            dic[i].append(os.stat(i).st_ctime)
            dic[i].append(os.stat(i).st_mtime)

    tituloInfo = 'Arquivos e Diretórios:'
    titulo_tamanho = '{:>5}'.format('Tamanho')
    titulo_data_criacao = '{:>30}'.format('Data de Criação')
    titulo_data_modificacao = '{:>38}'.format('Data de Modificação')
    titulo = titulo_tamanho + titulo_data_criacao + titulo_data_modificacao
    #print(titulo)
    textoTituloInfo = font.render(tituloInfo, 1, preto)
    tela.blit(textoTituloInfo, (20, 430))
    textoTitulo = font.render(titulo, 1, preto)
    tela.blit(textoTitulo, (20, 450))

    for i in dic:
        kb = dic[i][0]/1024
    tamanho = '{:>10}'.format(str('{:.2f}'.format(kb) + 'KB'))
    time_create = '{:>30}'.format(time.ctime(dic[i][0]))
    time_mod = '{:>30}'.format(time.ctime(dic[i][1]))
    nomeArquivo = '{:>30}'.format(i)
    textoArqDir = font.render(tamanho + time_create + time_mod
                              + nomeArquivo, 1, preto)
    tela.blit(textoArqDir, (20, 470))

def info_processo():
    s5.fill(branco)
    tela.blit(s5, (0, 5*alturaTela/6))
    p = psutil.Process(pid_selecionado)
    #print('\n''Nome do processo:', p.name())
    nameProcess = p.name()
    #print('Id do processo:', p.pid)
    processId = p.pid
    #print('Nome do usuário proprietário:',p.username())
    userName = p.username()
    data_criacao = datetime.datetime.fromtimestamp(p.create_time())\
        .strftime("%Y-%m-%d %H:%M:%S")
    #print('Data de criação do processo:', data_criacao)
    #print(p.memory_info())
    memInfo = p.memory_info()
    mem_usada = round(memInfo.rss/1024, 2)
    #print('Memória usada:', mem_usada,'KB')
    textoNameProcess = font.render('Nome do processo: ' + nameProcess, 1, preto)
    textoProcessId = font.render('Id do processo: ' + str(processId), 1, preto)
    textoUserName = font.render('Nome do usuário proprietário: ' + userName, 1, preto)
    textoDataCriacao = font.render('Data de criação: ' + data_criacao, 1, preto)
    textoMemInfo = font.render('Memória usada: ' + str(mem_usada), 1, preto)
    tela.blit(textoNameProcess, (20, 495))
    tela.blit(textoProcessId, (20, 515))
    tela.blit(textoUserName, (20, 535))
    tela.blit(textoDataCriacao, (20, 555))
    tela.blit(textoMemInfo, (20, 575))

list_pids = psutil.pids()
    #print('\n''Lista de processos em execução: ', list_pids)

for i in list_pids:
    pid_selecionado = i

if pid_selecionado in list_pids:
    info_processo()
else:
    print('PID selecionado não exite!')

# Repetição para capturar eventos e atualizar tela   
sair = False
while not sair:
    # Checar os eventos do mouse aqui:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = True
   
    # Fazer a atualização a cada segundo:
    if cont == 60:
        mostraInfoCpu()
        mostraUsoCpu(s0, listCpuPercent)
        mostraUsoMemoria()
        mostraUsoDisco()
        mostraIp()
        mostraInfoDir()
        info_processo()
        cont = 0 
                    
    # Atualiza o desenho na tela
    pygame.display.update()
      
    # 60 frames por segundo
    clock.tick(60)
    cont = cont + 1
   
# Finaliza a janela
pygame.display.quit()
pygame.quit() 