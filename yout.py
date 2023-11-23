from pytube import YouTube

def download_video(url, output_path='.'):
    try:
        # Cria um objeto YouTube com o URL do vídeo
        yt = YouTube(url)
        
        # Seleciona a melhor qualidade disponível
        video = yt.streams.get_highest_resolution()
        
        # Baixa o vídeo para o diretório especificado
        video.download(output_path)
        
        print(f"Download do vídeo {yt.title} concluído com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exemplo de uso
video_url = 'https://www.youtube.com/watch?v=DUJY5Z0TfeI&ab_channel=RELAXAR-DEITAREDORMIR'
download_video(video_url, 'C:\\Users\\Júlia\\OneDrive\\Documentos\\code\\yt')
