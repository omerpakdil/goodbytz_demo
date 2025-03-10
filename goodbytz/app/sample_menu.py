import logging

from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import SessionLocal
from app.models.menu_item import CategoryEnum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_menu(db: Session) -> None:
    # Appetizers
    appetizers = [
        {
            "name": "Mediterranean Salad",
            "description": "Fresh mixed greens with tomatoes, cucumbers, olives, feta cheese, and olive oil dressing.",
            "price": 45.0,
            "category": CategoryEnum.APPETIZER,
            "preparation_time": 10,
            "is_vegetarian": True,
            "is_vegan": False,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&auto=format&fit=crop"
        },
        {
            "name": "Lentil Soup",
            "description": "Traditional red lentil soup with carrots, onions, and special spices.",
            "price": 35.0,
            "category": CategoryEnum.APPETIZER,
            "preparation_time": 15,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800&auto=format&fit=crop"
        }
    ]
    
    # Main Courses
    main_courses = [
        {
            "name": "Grilled Salmon",
            "description": "Fresh salmon fillet grilled to perfection, served with seasonal vegetables and rice.",
            "price": 120.0,
            "category": CategoryEnum.MAIN_COURSE,
            "preparation_time": 25,
            "is_vegetarian": False,
            "is_vegan": False,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=800&auto=format&fit=crop"
        },
        {
            "name": "Vegetable Stir-Fry",
            "description": "Mixed seasonal vegetables stir-fried with tofu in a special sauce, served with rice.",
            "price": 75.0,
            "category": CategoryEnum.MAIN_COURSE,
            "preparation_time": 20,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&auto=format&fit=crop"
        }
    ]
    
    # Desserts
    desserts = [
        {
            "name": "Chocolate Brownie",
            "description": "Rich chocolate brownie served with vanilla ice cream and chocolate sauce.",
            "price": 45.0,
            "category": CategoryEnum.DESSERT,
            "preparation_time": 10,
            "is_vegetarian": True,
            "is_vegan": False,
            "is_gluten_free": False,
            "image_url": "https://images.unsplash.com/photo-1564355808539-22fda35bed7e?w=800&auto=format&fit=crop"
        },
        {
            "name": "Fruit Salad",
            "description": "Fresh seasonal fruits served with honey and mint leaves.",
            "price": 35.0,
            "category": CategoryEnum.DESSERT,
            "preparation_time": 10,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=800&auto=format&fit=crop"
        }
    ]
    
    # Drinks
    drinks = [
        {
            "name": "Fresh Orange Juice",
            "description": "Freshly squeezed orange juice.",
            "price": 20.0,
            "category": CategoryEnum.DRINK,
            "preparation_time": 5,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=800&auto=format&fit=crop"
        },
        {
            "name": "Turkish Coffee",
            "description": "Traditional Turkish coffee served with Turkish delight.",
            "price": 25.0,
            "category": CategoryEnum.DRINK,
            "preparation_time": 10,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1589410187794-8c8654e8e8a7?w=800&auto=format&fit=crop"
        }
    ]
    
    # Side Dishes
    side_dishes = [
        {
            "name": "French Fries",
            "description": "Crispy golden french fries served with special sauce.",
            "price": 30.0,
            "category": CategoryEnum.SIDE_DISH,
            "preparation_time": 15,
            "is_vegetarian": True,
            "is_vegan": True,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?w=800&auto=format&fit=crop"
        },
        {
            "name": "Tzatziki",
            "description": "Greek yogurt dip with cucumber, garlic, and herbs.",
            "price": 25.0,
            "category": CategoryEnum.SIDE_DISH,
            "preparation_time": 10,
            "is_vegetarian": True,
            "is_vegan": False,
            "is_gluten_free": True,
            "image_url": "https://images.unsplash.com/photo-1593001874117-c99c800e3eb8?w=800&auto=format&fit=crop"
        }
    ]
    
    # Combine all menu items
    all_items = appetizers + main_courses + desserts + drinks + side_dishes
    
    # Add menu items to database
    for item_data in all_items:
        # Check if item exists by name
        existing_item = db.query(crud.menu_item.model).filter(
            crud.menu_item.model.name == item_data["name"]
        ).first()
        
        if not existing_item:
            item_in = schemas.MenuItemCreate(**item_data)
            crud.menu_item.create(db, obj_in=item_in)
            logger.info(f"Menu item added: {item_data['name']}")
        else:
            logger.info(f"Menu item already exists: {item_data['name']}")


def main() -> None:
    logger.info("Adding sample menu items")
    db = SessionLocal()
    init_menu(db)
    logger.info("Sample menu items have been added")


if __name__ == "__main__":
    main() 