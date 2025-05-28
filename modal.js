document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal');
  const openBtn = document.querySelector('.open-modal-btn');
  const closeBtn = document.querySelector('.close-modal-btn');
  const form = document.getElementById('skate-form');

  // Открытие модалки
  openBtn.addEventListener('click', function() {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  });

  // Закрытие модалки
  closeBtn.addEventListener('click', function() {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
  });

  // Закрытие по клику вне модалки
  modal.addEventListener('click', function(e) {
    if (e.target === modal) {
      modal.classList.remove('show');
      document.body.style.overflow = 'auto';
    }
  });

  // Обработка отправки формы
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    console.log('Форма отправлена'); // Проверка срабатывания

    // Собираем данные формы
    const formData = {
      weight: document.getElementById('weight').value,
      budget: document.getElementById('budget').value,
      purposes: Array.from(document.querySelectorAll('input[name="purpose"]:checked'))
        .map(el => el.value)
    };

    console.log('Отправляемые данные:', formData); // Проверка собранных данных

    try {
      const response = await fetch('/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      console.log('Ответ сервера:', data); // Проверка ответа сервера

      if (data.success) {
        // Закрываем модалку
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';

        // Перенаправляем на страницу результатов
        window.location.href = '/results';
      } else {
        alert('Ошибка: ' + data.error);
      }
    } catch (error) {
      console.error('Ошибка при отправке:', error);
      alert('Произошла ошибка при отправке данных');
    }
  });
});