import matplotlib.pyplot as plt
import io

def plotar_grafico(media_total, pico_previsto, data_pico):
    fig, ax = plt.subplots()
    ax.bar(['População Atual', f'Pico Previsto\n({data_pico})'], [media_total, pico_previsto], color=['red', 'green'])
    ax.set_ylabel('Número médio de cigarrinhas')
    ax.set_title('População Atual vs Pico Previsto')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf