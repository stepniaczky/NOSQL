import uuid

from typing import List
from datetime import datetime, date

from src.models import Ticket, Client, Movie, ClientType
from src.db import get_collection


class TicketManager:

    @staticmethod
    def get_ticket(**query) -> Ticket or None:
        if not set(query.keys()).issubset(set(['_id', 'date', 'client_id', 'movie_id'])):
            print('Niepoprawne zapytanie!')
            return
        
        for key in ['_id', 'client_id', 'movie_id']:
            if key in query.keys():
                query[key] = str(query[key]) if isinstance(query[key], uuid.UUID) else query[key]
        
        tickets_collection = get_collection('tickets')
        res_list = list(tickets_collection.find(query))
        
        if len(res_list) == 0:
            print('Bilet o wskazanych parametrach nie istnieje!')
            return
        
        if len(res_list) > 1:
            print('Zapytanie zwróciło więcej niż jeden bilet!')
            return
        
        ticket = res_list[0]
        return Ticket(**ticket)

    @staticmethod
    def get_all_tickets() -> List[Ticket]:
        ticket_collection = get_collection('tickets')
        tickets_cursor = ticket_collection.find()
        
        tickets = []
        for ticket in tickets_cursor:
            tickets.append(Ticket(**ticket))
        
        return tickets

    @staticmethod
    def buy_ticket(client_id, movie_id):
        client_id = str(client_id) if isinstance(client_id, uuid.UUID) else client_id
        movie_id = str(movie_id) if isinstance(movie_id, uuid.UUID) else movie_id
        
        client_collection = get_collection('clients')
        movie_collection = get_collection('movies')
        ticket_collection = get_collection('tickets')
        
        client = client_collection.find_one({'_id': client_id})
        movie = movie_collection.find_one({'_id': movie_id})

        if client is None or movie is None:
            print('Podany użytkownik lub film nie istnieje!')
            return
        
        client_obj = Client(**client)
        movie_obj = Movie(**movie)

        if Client.get_age(client_obj.birth_date) < movie_obj.min_age:
            print('Użytkownik nie spełnia wymagań wiekowych!')
            return

        arr = movie_obj.free_slots
        slot_flag = False
        for i in range(1, len(arr) + 1):
            if movie_obj.set_free_slot(i):
                movie_collection.update_one({'_id': movie_id}, {'$set': {'free_slots': arr}})
                slot_flag = True
                break
            
        if not slot_flag:
            print('Brak wolnych miejsc na dany film!')
            return
        
        price = client_obj.client_type.apply_discount(25)
        _date = date.today().strftime('%d/%m/%Y')
        ticket = Ticket(date=_date,base_price=price,
                        client_id=client_obj._id, movie_id=movie_obj._id)
        ticket_collection.insert_one(ticket.__dict__())
        print('Pomyslnie dodano bilet o UUID: {}'.format(ticket._id))

    @staticmethod
    def get_size() -> int:
        ticket_collection = get_collection('tickets')
        return ticket_collection.count_documents({})