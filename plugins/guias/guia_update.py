import time
from core.config import C

METADATA = {
    "name": "Guia Avançado: S.O 2.4 (Air-Gapped via Proxmox)",
    "description": "Roteiro Operacional tático com alertas de saltstack, snapshots e tempos de janela.",
    "active": True
}

def run():
    print(f"\n{C.BOLD}{C.YELLOW}=== {METADATA['name']} ==={C.RESET}")
    
    print(f"\n{C.CYAN}[1] PREPARAÇÃO (ZONA LIMPA VS SUJA){C.RESET}")
    print("  - Valide obrigatoriamente a integridade SHA256 da ISO usando a ferramenta local na Zona Suja.")
    print("  - Insira a mídia na máquina física. Será montada no MPC e processada via console pelo 'soup'.")
    
    print(f"\n{C.CYAN}[2] MATRIZ DE DECISÃO DE SNAPSHOTS PROXMOX VE{C.RESET}")
    print("  +----------------------+----------------------------------------------------------------+")
    print("  | Com Memória (Live)   | Ideal p/ updates curtos (Docker/Salt). Retorna estado exato.  |")
    print("  | Sem Memória (Disk)   | Obrigatório p/ updates de Kernel do Core SO. Exige boot vazio.|")
    print("  +----------------------+----------------------------------------------------------------+")
    print("  (Aviso: discos em RAW LVM-Thick clássico não suportam snapshots. Requem clonagem pura).")
    
    print(f"\n{C.CYAN}[3] ORQUESTRAÇÃO DO UPDATER (SOUP){C.RESET}")
    print("  - Comando base via terminal no Manager: 'sudo soup -f /caminho/para/iso'")
    print("  - [AVISO] A atualização do Nó Manager DEVE OBRIGATORIAMENTE finalizar as tarefas")
    print("    e voltar ao shell antes que os Sensores (NIDS/Search) sejam tocados pelo Air-Gap.")
    
    print(f"\n{C.RED}[!] ALERTA CRÍTICO DE AUTENTICAÇÃO: SALTSTACK (v2.4.210){C.RESET}")
    print("  Regra de bloqueio do Salt mudou (minimum_auth_version=3). Se um nó distribuído (Sensor)")
    print("  falhar na update ou ficar travado e passar offline por mais de 7 DIAS...")
    print("  Ele será severamente rejeitado pelo Manager.")
    print("  Correção na GUI: Utilize a ferramenta do menu (Patch Auth Remoto SaltStack) neste script S.O.S.")
    
    print(f"\n{C.CYAN}[4] PÓS-ATUALIZAÇÃO & CHECK-IN (PACIÊNCIA TÁTICA){C.RESET}")
    print("  Os nós Air-Gapped possuem randomização de polling para checar em NIDS se há assinaturas ET Open.")
    print("  Eles podem demorar até 15 MINUTOS para compilar a janela de tráfego de update do Salt.")
    print("  Na dúvida da instabilidade, force recarga usando o Troubleshooting: 'sudo so-checkin' e 'so-status'.\n")
