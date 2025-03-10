document.addEventListener('DOMContentLoaded', function() {
    // Token kontrolü
    const token = localStorage.getItem('token');
    const userInfo = document.getElementById('user-info');
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const kitchenNav = document.getElementById('kitchen-nav');

    // Kullanıcı giriş durumunu kontrol et
    if (token) {
        // Kullanıcı bilgilerini getir
        fetch('/api/v1/users/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                // Token geçersiz, çıkış yap
                logout();
                throw new Error('Token geçersiz');
            }
        })
        .then(data => {
            if (userInfo) {
                userInfo.textContent = `Welcome, ${data.full_name || data.email}`;
                userInfo.style.display = 'block';
            }
            if (loginBtn) loginBtn.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'block';
            
            // Mutfak personeli kontrolü
            if (kitchenNav && (data.is_kitchen_staff || data.is_superuser)) {
                kitchenNav.style.display = 'block';
            } else if (kitchenNav) {
                kitchenNav.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Kullanıcı bilgileri alınamadı:', error);
        });
    } else {
        if (userInfo) userInfo.style.display = 'none';
        if (loginBtn) loginBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (kitchenNav) kitchenNav.style.display = 'none';
    }

    // Çıkış işlemi
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }

    function logout() {
        localStorage.removeItem('token');
        window.location.href = '/';
    }

    // Sipariş formu işleme
    const orderForm = document.getElementById('order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!token) {
                alert('Sipariş vermek için giriş yapmalısınız.');
                window.location.href = '/login';
                return;
            }
            
            const formData = new FormData(orderForm);
            const orderData = {
                items: [],
                notes: formData.get('notes'),
                table_number: parseInt(formData.get('table_number')) || null,
                is_takeaway: formData.get('is_takeaway') === 'on'
            };
            
            // Seçilen menü öğelerini topla
            const menuItems = document.querySelectorAll('.menu-item-checkbox:checked');
            menuItems.forEach(item => {
                const menuItemId = parseInt(item.value);
                const quantity = parseInt(document.getElementById(`quantity-${menuItemId}`).value) || 1;
                const specialInstructions = document.getElementById(`instructions-${menuItemId}`).value || '';
                
                orderData.items.push({
                    menu_item_id: menuItemId,
                    quantity: quantity,
                    special_instructions: specialInstructions
                });
            });

            console.log('Sipariş vermek için gönderilen veri:', orderData);
            
            
            // Siparişi gönder
            fetch('/api/v1/orders/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(orderData)
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Sipariş oluşturulamadı');
                }
            })
            .then(data => {
                alert('Siparişiniz başarıyla oluşturuldu!');
                window.location.href = `/orders/${data.id}`;
            })
            .catch(error => {
                console.error('Sipariş hatası:', error);
                alert('Sipariş oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.');
            });
        });
    }

    // Mutfak siparişleri güncelleme
    const updateOrderButtons = document.querySelectorAll('.update-order-status');
    if (updateOrderButtons.length > 0) {
        updateOrderButtons.forEach(button => {
            button.addEventListener('click', function() {
                const orderId = this.getAttribute('data-order-id');
                const status = this.getAttribute('data-status');
                
                fetch(`/api/v1/kitchen/orders/${orderId}/${status}`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Sipariş durumu güncellenemedi');
                    }
                })
                .then(data => {
                    alert('Sipariş durumu güncellendi!');
                    location.reload();
                })
                .catch(error => {
                    console.error('Güncelleme hatası:', error);
                    alert('Sipariş durumu güncellenirken bir hata oluştu.');
                });
            });
        });
    }
}); 