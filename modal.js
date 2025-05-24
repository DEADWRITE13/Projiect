document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('modal');
  const openBtn = document.querySelector('.open-modal-btn');
  const closeBtn = document.querySelector('.close-modal-btn');
  const form = document.getElementById('skate-form');

  // Открытие модалки
  openBtn.addEventListener('click', function() {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden'; // Блокируем скролл
  });

  // Закрытие модалки
  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function(e) {
    if (e.target === modal) closeModal();
  });

  // Обработка формы
  form.addEventListener('submit', function(e) {
    e.preventDefault();

    const data = {
      height: document.getElementById('height').value,
      weight: document.getElementById('weight').value,
      budget: document.getElementById('budget').value,
      footSize: document.getElementById('foot-size').value,
      purposes: Array.from(document.querySelectorAll('input[name="purpose"]:checked')).map(el => el.value)
    };

    console.log('Отправляем данные:', data);
    // Здесь будет AJAX-запрос к вашему Flask API
    closeModal();
  });

  function closeModal() {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
  }
});
form.addEventListener('submit', async function(e) {
  e.preventDefault();

  const formData = {
    height: document.getElementById('height').value,
    weight: document.getElementById('weight').value,
    budget: document.getElementById('budget').value,
    foot_size: document.getElementById('foot-size').value,
    purposes: Array.from(document.querySelectorAll('input[name="purpose"]:checked')).map(el => el.value)
  };

  try {
    const response = await fetch('/api/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData)
    });

    const result = await response.json();

    if (result.success) {
      // Обработка результатов (например, отображение в интерфейсе)
      displayRecommendations(result.recommendations);
      closeModal();
    } else {
      alert('Ошибка: ' + result.error);
    }
  } catch (error) {
    console.error('Ошибка сети:', error);
    alert('Ошибка соединения с сервером');
  }
});

function displayRecommendations(skateboards) {
  // Реализуйте отображение результатов на странице
  console.log('Получены рекомендации:', skateboards);
  // Пример: можно создать карточки товаров или таблицу
}