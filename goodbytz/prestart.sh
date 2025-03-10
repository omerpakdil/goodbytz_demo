#!/bin/bash

# Veritabanı migrasyonlarını çalıştır
echo "Veritabanı migrasyonları çalıştırılıyor..."
alembic upgrade head

# İlk kullanıcıları oluştur
echo "İlk kullanıcılar oluşturuluyor..."
python -m app.initial_data

# Örnek menü öğelerini ekle
echo "Örnek menü öğeleri ekleniyor..."
python -m app.sample_menu

echo "Başlatma işlemleri tamamlandı." 