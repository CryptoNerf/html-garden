import nodemailer from 'nodemailer';

export default async function handler(req, res) {
  // Разрешаем CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Логирование для отладки
    console.log('EMAIL_USER:', process.env.EMAIL_USER ? 'установлен' : 'НЕ УСТАНОВЛЕН');
    console.log('EMAIL_PASS:', process.env.EMAIL_PASS ? 'установлен' : 'НЕ УСТАНОВЛЕН');

    const { userName, plantName, plantDescription, userLocation, plantImage, plantImageName, userPhoto, userPhotoName } = req.body;

    // Проверка обязательных полей
    if (!userName || !plantImage) {
      return res.status(400).json({ error: 'Имя пользователя и изображение растения обязательны' });
    }

    console.log('Отправка письма от:', userName);

    // Создаем транспорт для Gmail
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER, // ваш Gmail
        pass: process.env.EMAIL_PASS, // пароль приложения Gmail
      },
    });

    // Подготовка вложений
    const attachments = [];

    // Добавляем изображение растения
    if (plantImage) {
      const plantImageData = plantImage.split(',')[1]; // Убираем data:image/png;base64,
      attachments.push({
        filename: plantImageName || 'plant.png',
        content: plantImageData,
        encoding: 'base64',
      });
    }

    // Добавляем селфи если есть
    if (userPhoto) {
      const userPhotoData = userPhoto.split(',')[1];
      attachments.push({
        filename: userPhotoName || 'user-photo.jpg',
        content: userPhotoData,
        encoding: 'base64',
      });
    }

    // Формируем HTML письма
    const emailHTML = `
      <div style="font-family: 'Comic Sans MS', cursive; color: #247b27; padding: 20px;">
        <h2 style="color: #f4d03f; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🌱 Новое растение для HTML-GARDEN!</h2>

        <div style="background-color: #f0f8f0; padding: 20px; border-radius: 10px; margin: 20px 0;">
          <h3 style="color: #247b27;">Информация о пользователе:</h3>
          <p><strong>Имя/Фамилия:</strong> ${userName}</p>
          ${userLocation ? `<p><strong>Откуда:</strong> ${userLocation}</p>` : ''}
        </div>

        <div style="background-color: #f0f8f0; padding: 20px; border-radius: 10px; margin: 20px 0;">
          <h3 style="color: #247b27;">Информация о растении:</h3>
          ${plantName ? `<p><strong>Имя растения:</strong> ${plantName}</p>` : '<p><em>Имя растения не указано</em></p>'}
          ${plantDescription ? `<p><strong>Описание:</strong> ${plantDescription}</p>` : '<p><em>Описание не указано</em></p>'}
        </div>

        <div style="background-color: #fff3cd; padding: 15px; border-radius: 10px; margin: 20px 0;">
          <h3 style="color: #247b27;">📎 Прикрепленные файлы:</h3>
          <ul>
            <li>Изображение растения: ${plantImageName || 'plant.png'}</li>
            ${userPhotoName ? `<li>Селфи: ${userPhotoName}</li>` : '<li><em>Селфи не прикреплено</em></li>'}
          </ul>
        </div>

        <p style="color: #888; font-size: 12px; margin-top: 30px;">
          Отправлено через форму HTML-GARDEN
        </p>
      </div>
    `;

    // Отправляем письмо
    await transporter.sendMail({
      from: `"HTML-GARDEN" <${process.env.EMAIL_USER}>`,
      to: 'emile.alexanyan@gmail.com',
      subject: `🌱 Новое растение от ${userName}`,
      html: emailHTML,
      attachments: attachments,
    });

    return res.status(200).json({ success: true, message: 'Email отправлен успешно!' });

  } catch (error) {
    console.error('Error sending email:', error);
    return res.status(500).json({ error: 'Ошибка при отправке email', details: error.message });
  }
}
