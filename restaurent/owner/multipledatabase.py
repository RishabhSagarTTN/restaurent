class OwnerRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'owner':
            return 'hello'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'owner':
            return 'hello'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
    
    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations between objects from different databases."""
        return True  
    
