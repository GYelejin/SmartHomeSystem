# Название проекта

МОСКОВСКАЯ ПРЕДПРОФЕССИОНАЛЬНАЯОЛИМПИАДА ШКОЛЬНИКОВ
Профиль «Информационные технологии»
Командный кейс № 7 «Умный дом»

Система умного дома с использованием Home Assistant

## Описание

Данный проект представляет собой систему умного дома, основанную на платформе Home Assistant. Система позволяет управлять различными устройствами в доме, такими как освещение, термостаты, замки, системы безопасности и другие, с помощью централизованного интерфейса.
По заданию кейсу необоходимо создать Компонент 5 для Конвертации сырых данных и Компонент 6 для переноса данных в систему управления базами данных на основе хранения временных рядов. Далее использование данных в системе визуализации - Grafana.
Далее:  

- Компонент 5 - Конвектор данных
- Компонент 6 - Переносчик данных в InfluxDB
  
## Требования

Для работы системы необходимо наличие следующих компонентов:

- Raspberry Pi или локальный сервер или менеджер виртуальных машин
- Устройства умного дома (например, умные лампы, термостаты, замки и т.д.)

## Установка и настройка

1. Установите Home Assistant.
2. Подключите устройства умного дома к системе, следуя инструкциям производителя каждого устройства.
3. Настройте систему умного дома через интерфейс Home Assistant, добавляя устройства и настраивая автоматизацию и сценарии в соответствии с вашими потребностями.
4. Для несовместимых устройств добавте конфигурацию в Конвектор данных
5. Запустить все компоненты

## Примеры использования

Ниже приведены некоторые примеры использования системы умного дома:

1. Управление освещением: Включайте и выключайте свет в разных комнатах или зонах дома с помощью мобильного приложения или голосовых команд.
2. Регулировка температуры: Устанавливайте и контролируйте температуру в доме с помощью термостатов, автоматически адаптируя ее в соответствии с вашим расписанием или погодными условиями.
3. Управление безопасностью: Получайте уведомления о взломах или необычной активности в доме, а также управляйте системами безопасности, такими как видеонаблюдение или сигнализация.
4. Создание сценариев: Создавайте сценарии для автоматического выполнения определенных действий, например, включение света и музыки при входе в дом или автоматическое закрытие штор по расписанию.

## Вклад в проект

Если вы хотите внести свой вклад в развитие проекта, вы можете:

- Создавать запросы на улучшение или исправление ошибок через систему управления задачами или путем создания запросов на слияние.
- Участвовать в обсуждениях и предлагать новые идеи или функциональности.
- Помогать другим пользователям, отвечая на их вопросы и предоставляя поддержку.

## Ссылки

- [Официальный сайт Home Assistant](https://www.home-assistant.io/)
- [Документация Home Assistant](https://www.home-assistant.io/docs/)
- [Сообщество Home Assistant](https://community.home-assistant.io/)
- [Брокер MQTT mosquitto](https://mosquitto.org/)  
- [БД InfluxDB](https://www.influxdata.com/)
