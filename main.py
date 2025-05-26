from datetime import datetime, timedelta
import google.generativeai as genai
from colorama import Fore, Style, init
import time
import random
import os

init(autoreset=True)

GOOGLE_API_KEY = "AIzaSyA58xYqJIL8kk4hYAL1OLnrQ0_MI80lYLI"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

MOTIVASYON_SOZLERI = [
    "🚀 Her yeni gün, yeni bir başlangıçtır!",
    "🌟 Bugün, hedeflerine bir adım daha yaklaşma günü!",
    "💡 Büyük işler küçük adımlarla başlar.",
    "🔥 Şimdi başla, mükemmel olmak zorunda değil!",
    "🎯 Disiplin, motivasyonun yerini alabilir!",
    "🌞 Her sabah, başarıya açılan yeni bir kapıdır.",
]

def temizle():
    os.system("cls" if os.name == "nt" else "clear")

def hosgeldin_mesaji():
    temizle()
    print(Fore.CYAN + Style.BRIGHT + "\n📅 Akıllı Günlük Planlayıcı'ya Hoş Geldin!\n")
    time.sleep(0.5)
    motivasyon = random.choice(MOTIVASYON_SOZLERI)
    print(Fore.LIGHTYELLOW_EX + f"{motivasyon}\n")
    time.sleep(1)

def gorevleri_al():
    print("🎯 Görevlerini sırayla gir. Bittiğinde sadece ENTER'a bas.\n")
    tasks = []
    while True:
        task = input("➤ Görev: ")
        if task.strip() == "":
            break
        while True:
            try:
                sure = int(input("  ⏱ Tahmini süre (dk): "))
                break
            except ValueError:
                print("  ❌ Lütfen geçerli bir sayı gir.")
        tasks.append((task.strip(), sure))
    return tasks

def baslangic_saati_al():
    while True:
        saat = input("⏰ Günü hangi saatte başlatmak istersin? (örn: 09:00): ").strip()
        try:
            datetime.strptime(saat, "%H:%M")
            return saat
        except ValueError:
            print("⚠️ Lütfen doğru formatta saat gir (örn: 08:30)")

def bitis_saati_al():
    while True:
        saat = input("🔚 Günü en geç hangi saatte bitirmek istersin? (örn: 18:00): ").strip()
        try:
            datetime.strptime(saat, "%H:%M")
            return saat
        except ValueError:
            print("⚠️ Lütfen doğru formatta saat gir (örn: 17:30)")

def saat_arti(saat, dakika):
    zaman = datetime.strptime(saat, "%H:%M")
    yeni_zaman = zaman + timedelta(minutes=dakika)
    return yeni_zaman.strftime("%H:%M")

def saat_farki_dakika(saat1, saat2):
    t1 = datetime.strptime(saat1, "%H:%M")
    t2 = datetime.strptime(saat2, "%H:%M")
    return int((t2 - t1).total_seconds() // 60)

def saatli_plan_olustur(tasks, baslangic_saati, bitis_saati, mola_suresi=10):
    toplam_gorev_suresi = sum(sure for _, sure in tasks)
    toplam_mola = mola_suresi * (len(tasks) - 1)
    gereken_toplam_sure = toplam_gorev_suresi + toplam_mola

    mevcut_sure = saat_farki_dakika(baslangic_saati, bitis_saati)
    bosluk = max(0, mevcut_sure - gereken_toplam_sure)
    aralik_sayisi = len(tasks) - 1
    extra_bosluk = bosluk // max(1, aralik_sayisi)

    plan = []
    simdiki_saat = baslangic_saati

    for i, (isim, sure) in enumerate(tasks):
        bitis = saat_arti(simdiki_saat, sure)
        plan.append((simdiki_saat, bitis, isim))
        simdiki_saat = bitis

        if i < len(tasks) - 1:
            simdiki_saat = saat_arti(simdiki_saat, mola_suresi + extra_bosluk)
            plan.append((bitis, simdiki_saat, "Mola"))

    return plan

def plan_ve_durum_goster(plan):
    temizle()
    print(Fore.GREEN + "📋 Saat Saat Günlük Plan:\n")
    for basla, bitir, gorev in plan:
        renk = Fore.LIGHTBLUE_EX if gorev == "Mola" else Fore.RESET
        print(f"{renk}🕘 {basla} - {bitir} → {gorev}")

def tamamlanan_gorevleri_isaretle(plan):
    print(Fore.CYAN + "\n✅ Tamamladığın görevleri işaretle (y = tamamlandı, diğer tuşlar = hayır):\n")
    tamamlandi, tamamlanmadi = [], []
    for i, (_, _, gorev) in enumerate(plan, 1):
        if gorev == "Mola":
            continue
        cevap = input(f"{i}. {gorev} - Tamamlandı mı? (y/n): ").strip().lower()
        if cevap == "y":
            tamamlandi.append(gorev)
        else:
            tamamlanmadi.append(gorev)
    return tamamlandi, tamamlanmadi

def tamamlanma_durumunu_goster(tamamlandi, tamamlanmadi):
    print(Fore.GREEN + "\n🎉 Tamamlanan Görevler:")
    for t in tamamlandi:
        print(f"✅ {t}")

    print(Fore.RED + "\n🕒 Tamamlanamayan Görevler:")
    for t in tamamlanmadi:
        print(f"❌ {t}")

def plan_dosyaya_kaydet(plan, tamamlandi, tamamlanmadi):
    with open("gunluk_plan.txt", "w", encoding="utf-8") as f:
        f.write("📋 Saat Saat Günlük Plan:\n")
        for basla, bitir, gorev in plan:
            f.write(f"{basla} - {bitir} → {gorev}\n")
        f.write("\n✅ Tamamlanan Görevler:\n")
        for t in tamamlandi:
            f.write(f"- {t}\n")
        f.write("\n❌ Tamamlanamayan Görevler:\n")
        for t in tamamlanmadi:
            f.write(f"- {t}\n")
    print(Fore.CYAN + "\n💾 Plan 'gunluk_plan.txt' dosyasına kaydedildi.")

def main():
    hosgeldin_mesaji()
    baslangic_saati = baslangic_saati_al()
    bitis_saati = bitis_saati_al()
    tasks = gorevleri_al()
    print(Fore.YELLOW + "\n⏳ Plan oluşturuluyor...\n")
    time.sleep(1)
    plan = saatli_plan_olustur(tasks, baslangic_saati, bitis_saati)
    plan_ve_durum_goster(plan)
    tamamlandi, tamamlanmadi = tamamlanan_gorevleri_isaretle(plan)
    tamamlanma_durumunu_goster(tamamlandi, tamamlanmadi)
    plan_dosyaya_kaydet(plan, tamamlandi, tamamlanmadi)
    print(Fore.MAGENTA + "\n💡 İpucu: Dinlenmek verimliliği artırır. Yarın görüşürüz! 👋")

if __name__ == "__main__":
    main()

