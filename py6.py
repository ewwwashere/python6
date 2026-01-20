from datetime import datetime

class Account:
    def __init__(self, account_holder, balance=0):
        # Проверяем, что начальный баланс не отрицательный
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным при создании счета")
        
        self.holder = account_holder  # Имя владельца
        self._balance = balance       # Приватный баланс
        self.operations_history = []  # Список всех операций
    
    def deposit(self, amount):
        # Пополнение счёта - сумма должна быть больше 0
        if amount <= 0:
            # Записываем неудачную попытку
            operation = {
                'type': 'deposit',
                'amount': amount,
                'timestamp': datetime.now(),
                'balance_after': self._balance,
                'status': 'fail'
            }
            self.operations_history.append(operation)
            return False
        
        # Успешное пополнение
        self._balance += amount
        operation = {
            'type': 'deposit',
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self._balance,
            'status': 'success'
        }
        self.operations_history.append(operation)
        return True
    
    def withdraw(self, amount):
        # Сумма должна быть положительной
        if amount <= 0:
            operation = {
                'type': 'withdraw',
                'amount': amount,
                'timestamp': datetime.now(),
                'balance_after': self._balance,
                'status': 'fail'
            }
            self.operations_history.append(operation)
            return False
        
        # Проверяем наличие денег
        if self._balance < amount:
            operation = {
                'type': 'withdraw',
                'amount': amount,
                'timestamp': datetime.now(),
                'balance_after': self._balance,
                'status': 'fail'
            }
            self.operations_history.append(operation)
            return False
        
        # Списание прошло успешно
        self._balance -= amount
        operation = {
            'type': 'withdraw',
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self._balance,
            'status': 'success'
        }
        self.operations_history.append(operation)
        return True
    
    def get_balance(self):
        """Возвращает текущий баланс"""
        return self._balance
    
    def get_history(self):
        """Возвращает копию истории операций (не оригинал)"""
        return self.operations_history.copy()

class CreditAccount(Account):
    def __init__(self, account_holder, balance=0, credit_limit=0):
        # Вызываем конструктор родителя
        super().__init__(account_holder, balance)
        self.credit_limit = credit_limit  # Кредитный лимит
    
    def withdraw(self, amount):
        # Проверяем положительность суммы
        if amount <= 0:
            operation = {
                'type': 'withdraw',
                'amount': amount,
                'timestamp': datetime.now(),
                'balance_after': self._balance,
                'status': 'fail',
                'used_credit': False
            }
            self.operations_history.append(operation)
            return False
        
        # Вычисляем доступную сумму (баланс + кредит)
        available = self._balance + self.credit_limit
        
        if available < amount:
            operation = {
                'type': 'withdraw',
                'amount': amount,
                'timestamp': datetime.now(),
                'balance_after': self._balance,
                'status': 'fail',
                'used_credit': False
            }
            self.operations_history.append(operation)
            return False
        
        # Определяем, использовался ли кредит
        used_credit = amount > self._balance
        self._balance -= amount
        
        operation = {
            'type': 'withdraw',
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self._balance,
            'status': 'success',
            'used_credit': used_credit
        }
        self.operations_history.append(operation)
        return True
    
    def get_available_credit(self):
        """Сколько еще можно снять (баланс + остаток кредита)"""
        return self._balance + self.credit_limit
    
    def get_history(self):
        # Добавляем поле used_credit для старых операций
        history = super().get_history()
        for op in history:
            if 'used_credit' not in op:
                op['used_credit'] = False
        return history
