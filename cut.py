from moviepy.editor import *

from moviepy.video.io.VideoFileClip import VideoFileClip

def cut_video(input_file, output_file, start_time, end_time):
    try:
        # Carrega o vídeo
        clip = VideoFileClip(input_file)
        
        # Corta o vídeo no intervalo desejado
        clipped = clip.subclip(start_time, end_time)
        
        # Salva o vídeo cortado
        clipped.write_videofile(output_file, codec="libx264", audio_codec="aac")
        
        print(f"Vídeo cortado com sucesso e salvo em {output_file}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")




# Exemplo de uso
input_file = 'C:\\Users\\Júlia\\OneDrive\\Documentos\\code\\yt\\BARULHO DE RODOVIA - BARULHO DE AVENIDA - SOM DE CARROS ACELERANDO - RELAXAR.mp4'
output_file = 'C:\\Users\\Júlia\\OneDrive\\Documentos\\code\\yt\\video.mp4'
start_time = 10  # Tempo inicial em segundos
end_time = 30    # Tempo final em segundos

cut_video(input_file, output_file, start_time, end_time)
