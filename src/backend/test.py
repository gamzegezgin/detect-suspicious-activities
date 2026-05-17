import os, sys
sys.path.append(r"C:\Users\acer\Desktop\tez kodları\detect-suspicious-activities\src\backend")
from predict import predict_video

VIDEOS_DIR = r"C:\Users\acer\Desktop\tez kodları\detect-suspicious-activities\src\frontend\videos"

dogru = 0
yanlis = 0

for fname in sorted(os.listdir(VIDEOS_DIR)):
    if not fname.endswith('.mp4'):
        continue
    
    # Gerçek etiket dosya adından al
    if 'fighting' in fname:
        gercek = 'Fighting'
    elif 'vandalism' in fname:
        gercek = 'Vandalism'
    elif 'normal' in fname:
        gercek = 'NormalVideos'
    else:
        continue
    
    sonuc = predict_video(os.path.join(VIDEOS_DIR, fname))
    tahmin = sonuc.get('label', '')
    
    if tahmin == gercek:
        dogru += 1
    else:
        yanlis += 1
        print(f"YANLIS: {fname} → Gerçek: {gercek}, Tahmin: {tahmin}")

print(f"\nDoğru: {dogru}, Yanlış: {yanlis}")
print(f"Accuracy: %{dogru/(dogru+yanlis)*100:.2f}")