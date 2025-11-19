from flask import render_template
import logging

logger = logging.getLogger(__name__)


def spec_byx():
    """Обработчик страницы специализации БУХ"""
    try:
        return render_template('specialization/byx.html')
    except Exception as e:
        logger.error(f"Ошибка загрузки шаблона: {e}")
        return "500 Internal Server Error", 500


def spec_po():
    """Обработчик страницы специализации ПО"""
    try:
        return render_template('specialization/po.html')
    except Exception as e:
        logger.error(f"Ошибка загрузки шаблона: {e}")
        return "500 Internal Server Error", 500


def spec_ogu():
    """Обработчик страницы специализации ОГУ"""
    try:
        return render_template('specialization/ogu.html')
    except Exception as e:
        logger.error(f"Ошибка загрузки шаблона: {e}")
        return "500 Internal Server Error", 500


def spec_do():
    """Обработчик страницы специализации ДО"""
    try:
        return render_template('specialization/do.html')
    except Exception as e:
        logger.error(f"Ошибка загрузки шаблона: {e}")
        return "500 Internal Server Error", 500


def spec_soc_rab():
    """Обработчик страницы специализации Соц. Раб"""
    try:
        return render_template('specialization/soc_rab.html')
    except Exception as e:
        logger.error(f"Ошибка загрузки шаблона: {e}")
        return "500 Internal Server Error", 500

