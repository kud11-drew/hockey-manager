# -*- coding: utf-8 -*-
"""
HOCKEY MANAGER MOBILE — Kivy версия для Android
Сборка в APK через buildozer (см. buildozer.spec в конце файла)
"""

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', '1')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import (Color, Ellipse, Rectangle, Line, RoundedRectangle,
                            Triangle, Polygon, PushMatrix, PopMatrix, Rotate)
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.properties import (NumericProperty, StringProperty, ListProperty,
                              ObjectProperty, BooleanProperty)
import random, math, json, os

# ==================== ЦВЕТА ====================
def c(h): return get_color_from_hex(h)

BG      = c('#0a1828')
PANEL   = c('#12263f')
PANEL2  = c('#1a3352')
PANEL3  = c('#26466b')
ACCENT  = c('#4fc3f7')
ACCENT2 = c('#ff5252')
GOLD    = c('#ffd54f')
TEXT    = c('#e3f2fd')
MUTED   = c('#7a94ab')
GREEN   = c('#66bb6a')
RED     = c('#ef5350')
WHITE   = c('#ffffff')
ICE     = c('#80deea')
DARK    = c('#050d18')

Window.clearcolor = BG

# ==================== ДАННЫЕ ====================
def make_name_ru():
    f = random.choice(['Александр','Дмитрий','Максим','Иван','Артём','Никита','Егор','Михаил','Роман','Даниил','Кирилл','Андрей','Сергей','Павел','Глеб','Лев'])
    l = random.choice(['Иванов','Петров','Смирнов','Кузнецов','Соколов','Попов','Лебедев','Козлов','Новиков','Морозов','Волков','Зайцев','Фёдоров','Орлов'])
    return f"{f} {l}"

def make_name_en():
    f = random.choice(['Connor','Nathan','Tyler','Ryan','Jack','Cole','Owen','Liam','Noah','Ethan','Logan','Dylan','Luke'])
    l = random.choice(['McAllister','MacGregor','Bertrand','Leclerc','Boucher','Fontaine','Marchand','Gagnon','Lefebvre','Pelletier','Tremblay','Dupont'])
    return f"{f} {l}"

KHL_TEAMS = [
    ('Лада','Тольятти','West','ЛАД','#003d82','#ffcc00',70,68),
    ('СКА','СПб','West','СКА','#003087','#c8102e',88,85),
    ('Сочи','Сочи','West','СОЧ','#00563f','#00a859',72,70),
    ('Спартак','Москва','West','СПА','#d7141a','#ffffff',78,75),
    ('Торпедо','НН','West','ТОР','#0066b3','#ffffff',76,74),
    ('Динамо','Минск','West','ДМН','#0d47a1','#ffffff',74,72),
    ('Динамо','Москва','West','ДИН','#1e3a8a','#ffffff',85,82),
    ('Локомотив','Ярославль','West','ЛОК','#c8102e','#003d82',82,80),
    ('Северсталь','Череповец','West','СЕВ','#f5c518','#003d82',71,70),
    ('ЦСКА','Москва','West','ЦСК','#c8102e','#1e3a8a',87,84),
    ('Шанхай','Шанхай','West','ШАН','#e60012','#ffcc00',73,71),
    ('Автомобилист','Екб','East','АВТ','#004a99','#ffffff',80,78),
    ('Ак Барс','Казань','East','АКБ','#00843d','#ffffff',85,82),
    ('Металлург','Магнитка','East','МЕТ','#003d82','#ffcc00',84,82),
    ('Нефтехимик','Нижнекамск','East','НЕФ','#008d36','#ffffff',70,69),
    ('Трактор','Челябинск','East','ТРА','#002d5b','#ffffff',77,76),
    ('Авангард','Омск','East','АВА','#d7141a','#000000',81,79),
    ('Адмирал','Владивосток','East','АДМ','#004a99','#ffffff',70,68),
    ('Амур','Хабаровск','East','АМУ','#1a3a6e','#f5c518',68,67),
    ('Барыс','Астана','East','БАР','#00a6e0','#f5c518',72,70),
    ('Салават','Уфа','East','САЛ','#00529b','#ffffff',82,79),
    ('Сибирь','Новосибирск','East','СИБ','#0e4c92','#ffffff',74,73),
]

NHL_TEAMS = [
    ('Бостон','Бостон','East','БОС','#ffb81c','#000000',84,82),
    ('Баффало','Баффало','East','БАФ','#003087','#ffb81c',76,74),
    ('Детройт','Детройт','East','ДТР','#ce1126','#ffffff',79,78),
    ('Флорида','Санрайз','East','ФЛО','#c8102e','#041e42',87,84),
    ('Монреаль','Монреаль','East','МНР','#af1e2d','#192168',78,76),
    ('Оттава','Оттава','East','ОТТ','#c8102e','#000000',77,75),
    ('Тампа','Тампа','East','ТБЛ','#002868','#ffffff',85,83),
    ('Торонто','Торонто','East','ТРН','#00205b','#ffffff',86,82),
    ('Вашингтон','Вашингтон','East','ВШГ','#c8102e','#041e42',82,79),
    ('Каролина','Роли','East','КРЛ','#cc0000','#000000',84,82),
    ('Коламбус','Коламбус','East','КЛБ','#002654','#ce1126',76,74),
    ('Нью-Джерси','Ньюарк','East','НДД','#ce1126','#000000',82,80),
    ('Айлендерс','Нью-Йорк','East','НЙА','#00539b','#f47a38',77,77),
    ('Рейнджерс','Нью-Йорк','East','НЙР','#0038a8','#ce1126',85,82),
    ('Питтсбург','Питтсбург','East','ПТТ','#fcb514','#000000',80,78),
    ('Филадельфия','Филадельфия','East','ФЛД','#f74902','#000000',78,76),
    ('Виннипег','Виннипег','West','ВНП','#041e42','#004c97',83,82),
    ('Даллас','Даллас','West','ДЛС','#006847','#111111',85,83),
    ('Колорадо','Денвер','West','КЛР','#6f263d','#236192',87,84),
    ('Миннесота','Сент-Пол','West','МНС','#154734','#a6192e',82,80),
    ('Нэшвилл','Нэшвилл','West','НШВ','#ffb81c','#041e42',80,79),
    ('Сент-Луис','Сент-Луис','West','СТЛ','#002f87','#fcb514',79,78),
    ('Чикаго','Чикаго','West','ЧКГ','#cf0a2c','#000000',72,71),
    ('Юта','Солт-Лейк','West','ЮТА','#71afe5','#000000',74,74),
    ('Анахайм','Анахайм','West','АНХ','#f47a38','#b9975b',74,73),
    ('Ванкувер','Ванкувер','West','ВНК','#00205b','#00843d',82,80),
    ('Вегас','Лас-Вегас','West','ВГС','#b4975a','#333f42',84,83),
    ('Калгари','Калгари','West','КЛГ','#d2001c','#f1be48',77,76),
    ('Лос-Анджелес','ЛА','West','ЛАК','#111111','#a2aaad',82,80),
    ('Сан-Хосе','Сан-Хосе','West','СХШ','#006d75','#ea7200',72,71),
    ('Сиэтл','Сиэтл','West','СЭТ','#001628','#99d9d9',76,75),
    ('Эдмонтон','Эдмонтон','West','ЭДМ','#041e42','#ff4c00',86,82),
]

VHL_TEAMS = [
    ('АКМ','Тула','VHL','АКМ','#1a3a6e','#f5c518',70,68),
    ('Барс','Казань','VHL','БРС','#00843d','#ffffff',67,66),
    ('Буран','Воронеж','VHL','БУР','#c8102e','#ffffff',68,67),
    ('Горняк','В.Пышма','VHL','ГРН','#d4af37','#000000',66,65),
    ('Дизель','Пенза','VHL','ДЗЛ','#003d82','#ffffff',65,64),
    ('Динамо-Алтай','Барнаул','VHL','ДЛА','#1e3a8a','#ffffff',66,65),
    ('Зауралье','Курган','VHL','ЗУР','#003d82','#ffcc00',68,67),
    ('Звезда','Москва','VHL','ЗВД','#c8102e','#1e3a8a',69,68),
    ('Ижсталь','Ижевск','VHL','ИЖС','#1e3a8a','#c8102e',64,63),
    ('Кристалл','Саратов','VHL','КРС','#003d82','#ffffff',63,62),
    ('Магнитка','Магнитка','VHL','МГН','#003d82','#ffcc00',71,70),
    ('Металлург','Новокузнецк','VHL','МНК','#1e3a8a','#c8102e',70,69),
    ('Молот','Пермь','VHL','МЛТ','#00843d','#ffffff',66,65),
    ('Нефтяник','Альметьево','VHL','НФТ','#008d36','#ffffff',69,68),
    ('Олимпия','Кирово-Чепецк','VHL','ОЛМ','#003d82','#ffffff',63,62),
    ('Омские Крылья','Омск','VHL','ОКР','#d7141a','#000000',70,69),
    ('Рубин','Тюмень','VHL','РБН','#003d82','#ffcc00',71,70),
    ('Сокол','Красноярск','VHL','СКЛ','#c8102e','#ffffff',68,67),
    ('Торос','Нефтекамск','VHL','ТРС','#00843d','#ffffff',67,66),
    ('Химик','Воскресенск','VHL','ХМК','#003d82','#ffcc00',66,65),
    ('ЦСК ВВС','Самара','VHL','ЦВС','#c8102e','#1e3a8a',65,64),
    ('Челмет','Челябинск','VHL','ЧЛМ','#002d5b','#ffffff',68,67),
    ('Югра','Ханты-Манс','VHL','ЮГР','#00529b','#ffffff',72,71),
    ('Южный Урал','Орск','VHL','ЮУР','#003d82','#ffcc00',67,66),
]

LEAGUES = {
    'KHL': {'name':'КХЛ','teams':KHL_TEAMS,'matches':68,'cup':'Кубка Гагарина','flag':'RU'},
    'NHL': {'name':'НХЛ','teams':NHL_TEAMS,'matches':84,'cup':'Кубка Стэнли','flag':'US'},
    'VHL': {'name':'ВХЛ','teams':VHL_TEAMS,'matches':58,'cup':'Кубка Петрова','flag':'RU'},
}

# ==================== ЛОГИКА ====================
class Player:
    _id_counter = 1
    def __init__(self, name, pos, skill, age=18):
        self.pid = Player._id_counter; Player._id_counter += 1
        self.name = name; self.pos = pos; self.skill = skill; self.age = age
        self.potential = min(99, skill + random.randint(3, 18))
        self.stamina = 100; self.morale = random.randint(60, 85)
        self.goals = 0; self.assists = 0; self.games = 0
        self.injury = 0
    def eff(self):
        if self.injury > 0: return 0
        return self.skill * (0.55 + 0.45 * self.stamina / 100) * (0.85 + 0.15 * self.morale / 100)

class Team:
    def __init__(self, data, is_user=False):
        self.name, self.city, self.conf, self.abbr, self.color1, self.color2, atk, df = data
        self.base_attack = atk
        self.base_defense = df
        self.budget = 500 + random.randint(0, 1500)
        self.is_user = is_user
        self.players = []
        self.wins = 0; self.losses = 0; self.ot_losses = 0
        self.points = 0; self.gf = 0; self.ga = 0
        self.titles = 0
        self.trust = 55

    def gen_roster(self, is_nhl=False):
        ov = (self.base_attack + self.base_defense) / 2
        avg = int(ov * 0.95)
        mn = max(30, avg - 15); mx = min(95, avg + 15)
        for _ in range(2):
            self.players.append(Player(make_name_en() if is_nhl else make_name_ru(), 'G', random.randint(mn-5, mx-5), random.randint(20, 33)))
        for _ in range(8):
            self.players.append(Player(make_name_en() if is_nhl else make_name_ru(), 'D', random.randint(mn, mx), random.randint(18, 33)))
        for _ in range(12):
            self.players.append(Player(make_name_en() if is_nhl else make_name_ru(), 'F', random.randint(mn, mx), random.randint(18, 33)))

    def strength(self):
        act = [p for p in self.players if p.injury == 0]
        if not act: return 30
        top = sorted(act, key=lambda p: -p.eff())[:6]
        return sum(p.eff() for p in top) / len(top)

class MatchSim:
    def __init__(self, home, away):
        self.home = home; self.away = away
        self.hs = 0; self.aws = 0
        self.minute = 0; self.period = 1
        self.phase = 'regulation'
        self.events = []

    def step(self):
        if self.phase == 'done': return []
        evts = []
        if self.phase == 'regulation':
            self.minute += 1
            self._minute_events(evts)
            if self.minute == 20:
                self.period = 2
                evts.append({'type':'period','text':f'Перерыв после 1-го: {self.hs}:{self.aws}'})
            elif self.minute == 40:
                self.period = 3
                evts.append({'type':'period','text':f'Перерыв после 2-го: {self.hs}:{self.aws}'})
            elif self.minute >= 60:
                if self.hs == self.aws:
                    self.phase = 'ot'; self.minute = 0
                    evts.append({'type':'period','text':'ОВЕРТАЙМ!'})
                else:
                    self.phase = 'done'
                    evts.append({'type':'period','text':f'Матч завершён: {self.hs}:{self.aws}'})
        elif self.phase == 'ot':
            self.minute += 1
            if random.random() < 0.1:
                diff = (self.home.strength() - self.away.strength()) / 18
                if random.random() < 0.5 + diff / 200:
                    self.hs += 1
                    scorer = self._pick_scorer(self.home)
                    evts.append({'type':'goal','text':f"ОТ: {scorer.name} — {self.home.name}",'team':'home'})
                else:
                    self.aws += 1
                    scorer = self._pick_scorer(self.away)
                    evts.append({'type':'goal','text':f"ОТ: {scorer.name} — {self.away.name}",'team':'away'})
                self.phase = 'done'
            elif self.minute >= 5:
                self.phase = 'shootout'
                evts.append({'type':'period','text':'БУЛЛИТЫ!'})
        elif self.phase == 'shootout':
            for i in range(5):
                if random.random() < 0.35: self.hs += 1
                if random.random() < 0.35: self.aws += 1
            self.phase = 'done'
            w = self.home.name if self.hs > self.aws else self.away.name
            evts.append({'type':'period','text':f'Буллиты: {w} ({self.hs}:{self.aws})'})
        return evts

    def _minute_events(self, evts):
        r = random.random()
        if r < 0.07:
            diff = (self.home.strength() - self.away.strength()) / 18
            if random.random() < 0.5 + diff / 200:
                self.hs += 1
                scorer = self._pick_scorer(self.home)
                evts.append({'type':'goal','text':f"{self.minute}' ГОЛ! {scorer.name} — {self.home.name}",'team':'home'})
            else:
                self.aws += 1
                scorer = self._pick_scorer(self.away)
                evts.append({'type':'goal','text':f"{self.minute}' ГОЛ! {scorer.name} — {self.away.name}",'team':'away'})
        elif r < 0.10:
            team = random.choice([self.home, self.away])
            pool = [p for p in team.players if p.injury == 0 and p.pos != 'G']
            if pool:
                p = random.choice(pool)
                evts.append({'type':'penalty','text':f"{self.minute}' Удаление: {p.name}"})

    def _pick_scorer(self, team):
        pool = [p for p in team.players if p.injury == 0 and p.pos != 'G']
        if not pool: return team.players[0]
        return random.choices(pool, weights=[p.eff() for p in pool])[0]

class Game:
    def __init__(self, league_key, user_idx):
        self.league_key = league_key
        L = LEAGUES[league_key]
        self.teams = []
        self.user_idx = user_idx
        for i, d in enumerate(L['teams']):
            t = Team(d, is_user=(i == user_idx))
            t.gen_roster(is_nhl=(league_key == 'NHL'))
            self.teams.append(t)
        self.season = 1
        self.day = 0
        self.history = []
        self.calendar = self._make_calendar()
        self.playoff_bracket = None
        self.playoff_stage = None
        self.champion = None
        self.champions_history = []

    @property
    def user(self): return self.teams[self.user_idx]

    def _make_calendar(self):
        n = len(self.teams)
        total = LEAGUES[self.league_key]['matches']
        ids = list(range(n))
        base = []
        for r in range(n - 1):
            rnd = []
            for i in range(n // 2):
                a, b = ids[i], ids[n - 1 - i]
                rnd.append((a, b) if (r + i) % 2 == 0 else (b, a))
            base.append(rnd)
            ids = [ids[0]] + [ids[-1]] + ids[1:-1]
        second = [[(b, a) for a, b in rnd] for rnd in base]
        sched = base + second
        extra = total - len(sched)
        for _ in range(extra):
            pool = list(range(n)); random.shuffle(pool)
            rnd = []
            while len(pool) >= 2:
                a = pool.pop(); b = pool.pop()
                rnd.append((a, b))
            sched.append(rnd)
        return sched

    def next_day(self):
        if self.day >= len(self.calendar):
            return {'done': True}
        rnd = self.calendar[self.day]
        results = []
        user_pending = None
        for a, b in rnd:
            if a == self.user_idx or b == self.user_idx:
                user_pending = (a, b)
                continue
            r = self._quick_sim(self.teams[a], self.teams[b])
            self.history.append(r)
            results.append(r)
        self.day += 1
        return {'done': False, 'results': results, 'user_pending': user_pending}

    def _quick_sim(self, home, away):
        hs = home.strength() + 2
        aw = away.strength()
        diff = (hs - aw) / 18
        hg = max(0, int(random.gauss(2.7 + diff, 1.3)))
        ag = max(0, int(random.gauss(2.7 - diff, 1.3)))
        home.gf += hg; home.ga += ag
        away.gf += ag; away.ga += hg
        if hg > ag:
            home.wins += 1; home.points += 3; away.losses += 1
        elif hg < ag:
            away.wins += 1; away.points += 3; home.losses += 1
        else:
            if random.random() < 0.5: home.points += 2; away.points += 1
            else: away.points += 2; home.points += 1
        return {'home_id': self.teams.index(home), 'away_id': self.teams.index(away),
                'home_name': home.name, 'away_name': away.name,
                'home_goals': hg, 'away_goals': ag}

    def user_play_match(self, home_id, away_id):
        home = self.teams[home_id]; away = self.teams[away_id]
        sim = MatchSim(home, away)
        while sim.phase != 'done':
            sim.step()
        hg, ag = sim.hs, sim.aws
        home.gf += hg; home.ga += ag
        away.gf += ag; away.ga += hg
        if hg > ag: home.wins += 1; home.points += 3; away.losses += 1
        elif hg < ag: away.wins += 1; away.points += 3; home.losses += 1
        else:
            if random.random() < 0.5: home.points += 2; away.points += 1
            else: away.points += 2; home.points += 1
        self.history.append({'home_id': home_id, 'away_id': away_id,
                              'home_name': home.name, 'away_name': away.name,
                              'home_goals': hg, 'away_goals': ag})
        return sim

    def start_playoffs(self):
        if self.playoff_stage: return
        def top8(conf):
            return sorted([t for t in self.teams if t.conf == conf],
                          key=lambda t: (-t.points, -(t.gf - t.ga), t.name))[:8]
        bracket = {}
        if self.league_key in ('KHL', 'NHL'):
            for conf in ('West', 'East'):
                top = top8(conf)
                if len(top) < 8: continue
                series = []
                for i in range(4):
                    a, b = top[i], top[7 - i]
                    series.append({'a': self.teams.index(a), 'b': self.teams.index(b),
                                    'wins_a': 0, 'wins_b': 0, 'games': []})
                bracket[conf] = {'stage': '1/4' if self.league_key == 'KHL' else '1/8', 'series': series}
        else:
            top = sorted(self.teams, key=lambda t: (-t.points, -(t.gf - t.ga), t.name))[:16]
            series = []
            for i in range(len(top) // 2):
                a, b = top[i], top[len(top) - 1 - i]
                series.append({'a': self.teams.index(a), 'b': self.teams.index(b),
                                'wins_a': 0, 'wins_b': 0, 'games': []})
            bracket = {'VHL': {'stage': '1/8', 'series': series}}
        self.playoff_bracket = bracket
        self.playoff_stage = 'r1'

    def advance_playoff(self):
        st = self.playoff_stage
        if st == 'done': return
        all_done = True
        for conf, data in self.playoff_bracket.items():
            for s in data['series']:
                if s['wins_a'] < 4 and s['wins_b'] < 4:
                    all_done = False; break
            if not all_done: break
        if not all_done: return
        winners = {conf: [s['a'] if s['wins_a'] == 4 else s['b'] for s in data['series']]
                   for conf, data in self.playoff_bracket.items()}
        if st == 'r1':
            if self.league_key == 'VHL':
                w = winners['VHL']
                new = {'VHL': {'stage': '1/4', 'series': [
                    {'a': w[0], 'b': w[1], 'wins_a': 0, 'wins_b': 0, 'games': []},
                    {'a': w[2], 'b': w[3], 'wins_a': 0, 'wins_b': 0, 'games': []},
                    {'a': w[4], 'b': w[5], 'wins_a': 0, 'wins_b': 0, 'games': []},
                    {'a': w[6], 'b': w[7], 'wins_a': 0, 'wins_b': 0, 'games': []}]}}
            else:
                new = {}
                for conf in winners:
                    w = winners[conf]
                    new[conf] = {'stage': '1/4', 'series': [
                        {'a': w[0], 'b': w[1], 'wins_a': 0, 'wins_b': 0, 'games': []},
                        {'a': w[2], 'b': w[3], 'wins_a': 0, 'wins_b': 0, 'games': []}]}
            self.playoff_bracket = new
            self.playoff_stage = 'r2'
        elif st == 'r2':
            new = {}
            for conf in winners:
                w = winners[conf]
                new[conf] = {'stage': '1/2', 'series': [
                    {'a': w[0], 'b': w[1], 'wins_a': 0, 'wins_b': 0, 'games': []}]}
            self.playoff_bracket = new
            self.playoff_stage = 'r3'
        elif st == 'r3':
            new = {}
            for conf in winners:
                w = winners[conf]
                new[conf] = {'stage': 'Финал конф.', 'series': [
                    {'a': w[0], 'b': w[1], 'wins_a': 0, 'wins_b': 0, 'games': []}]}
            self.playoff_bracket = new
            self.playoff_stage = 'conf_final'
        elif st == 'conf_final':
            cc = [winners[conf][0] for conf in winners]
            self.playoff_bracket = {'Cup': {'stage': 'Финал', 'series': [
                {'a': cc[0], 'b': cc[1], 'wins_a': 0, 'wins_b': 0, 'games': []}]}}
            self.playoff_stage = 'cup'
        elif st == 'cup':
            s = self.playoff_bracket['Cup']['series'][0]
            if s['wins_a'] == 4 or s['wins_b'] == 4:
                w = s['a'] if s['wins_a'] == 4 else s['b']
                self.champion = self.teams[w]
                self.champion.titles += 1
                self.champions_history.append({'season': self.season, 'team': self.champion.name})
                self.playoff_stage = 'done'

    def sim_playoff_stage(self):
        if self.playoff_stage == 'done' or not self.playoff_bracket: return
        for conf in list(self.playoff_bracket.keys()):
            for s in self.playoff_bracket[conf]['series']:
                while s['wins_a'] < 4 and s['wins_b'] < 4:
                    a = self.teams[s['a']]; b = self.teams[s['b']]
                    g = s['wins_a'] + s['wins_b']
                    home, away = (a, b) if g % 2 == 0 else (b, a)
                    r = self._quick_sim(home, away)
                    s['games'].append(r)
                    if r['home_goals'] > r['away_goals']: w = r['home_id']
                    else: w = r['away_id']
                    if w == s['a']: s['wins_a'] += 1
                    else: s['wins_b'] += 1
        self.advance_playoff()

    def standings(self):
        return sorted(self.teams, key=lambda t: (-t.points, -(t.gf - t.ga), t.name))

    def conf_standings(self, conf):
        return sorted([t for t in self.teams if t.conf == conf],
                      key=lambda t: (-t.points, -(t.gf - t.ga), t.name))


# ==================== WIDGETS ====================
def hexstr(h): return get_color_from_hex(h)


class LogoWidget(Widget):
    """Рисует щит-логотип с аббревиатурой."""
    color1 = StringProperty('#1e6fdb')
    color2 = StringProperty('#ffffff')
    abbr = StringProperty('')

    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(pos=self.redraw, size=self.redraw)
        self.bind(color1=self.redraw, color2=self.redraw, abbr=self.redraw)
        Clock.schedule_once(self.redraw, 0)

    def redraw(self, *a):
        self.canvas.clear()
        if not self.abbr: return
        cx, cy = self.center_x, self.center_y
        s = min(self.width, self.height) * 0.45
        with self.canvas:
            # тень
            Color(0, 0, 0, 0.4)
            Ellipse(pos=(cx - s * 1.05, cy - s * 1.15), size=(s * 2.1, s * 2.1))
            # внешний щит
            c2 = hexstr(self.color2)
            Color(*c2)
            pts = [
                cx - s, cy + s * 0.75,
                cx, cy + s,
                cx + s, cy + s * 0.75,
                cx + s * 0.75, cy - s * 0.75,
                cx, cy - s * 1.15,
                cx - s * 0.75, cy - s * 0.75,
            ]
            Polygon(points=pts)
            # внутренний щит
            c1 = hexstr(self.color1)
            Color(*c1)
            s2 = s * 0.85
            pts2 = [
                cx - s2, cy + s2 * 0.75,
                cx, cy + s2,
                cx + s2, cy + s2 * 0.75,
                cx + s2 * 0.75, cy - s2 * 0.75,
                cx, cy - s2 * 1.15,
                cx - s2 * 0.75, cy - s2 * 0.75,
            ]
            Polygon(points=pts2)
            # блик
            Color(1, 1, 1, 0.15)
            Ellipse(pos=(cx - s * 0.6, cy + s * 0.1), size=(s * 1.2, s * 0.7))
            # аббревиатура
            Color(1, 1, 1, 1)
            from kivy.core.text import Label as CoreLabel
            lbl = CoreLabel(text=self.abbr, font_size=int(s * 0.55), bold=True)
            lbl.refresh()
            tex = lbl.texture
            Color(1, 1, 1, 1)
            Rectangle(texture=tex, pos=(cx - tex.width / 2, cy - tex.height / 2),
                      size=tex.size)


class PuckWidget(Widget):
    """Анимированная шайба с пламенем."""
    frame = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(pos=self.redraw, size=self.redraw)
        Clock.schedule_interval(self.tick, 0.05)

    def tick(self, dt):
        self.frame += 1
        self.redraw()

    def redraw(self, *a):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.28
        f = self.frame
        with self.canvas:
            # свечение
            glow = r + math.sin(f / 3) * 4
            Color(0.05, 0.15, 0.35, 0.3)
            Ellipse(pos=(cx - glow * 1.6, cy - glow * 1.4), size=(glow * 3.2, glow * 2.8))
            Color(0.1, 0.3, 0.6, 0.25)
            Ellipse(pos=(cx - glow * 1.3, cy - glow * 1.15), size=(glow * 2.6, glow * 2.3))
            Color(0.2, 0.5, 0.9, 0.2)
            Ellipse(pos=(cx - glow, cy - glow * 0.9), size=(glow * 2, glow * 1.8))
            # пламя — 3 слоя полигонов
            for layer, (color, scale) in enumerate([(ACCENT, 1.0), (ICE, 0.75), (WHITE, 0.4)]):
                pts = []
                n = 14
                for i in range(n + 1):
                    t = i / n
                    x = cx - r * 1.1 * scale + 2.2 * r * scale * t
                    wave = math.sin(t * math.pi * 4 + f / 5 + layer) * r * 0.12
                    wave += math.sin(t * math.pi * 7 + f / 3) * r * 0.06
                    y = cy - wave - (1 - t * 0.3) * layer * r * 0.15 - t * r * 0.12
                    pts.extend([x, y])
                pts.extend([cx + r * 1.1 * scale, cy + r * 0.3, cx - r * 1.1 * scale, cy + r * 0.3])
                Color(*color)
                Polygon(points=pts)
            # шайба
            Color(0.02, 0.02, 0.02)
            Ellipse(pos=(cx - r, cy - r * 0.4), size=(r * 2, r * 1.4))
            Color(0.12, 0.12, 0.12)
            Ellipse(pos=(cx - r * 0.85, cy - r * 0.25), size=(r * 1.7, r * 1.1))
            Color(0.4, 0.4, 0.4, 0.5)
            Line(circle=(cx, cy + r * 0.15, r * 0.4), width=1.5)


class HockeyButton(ButtonBehavior, Label):
    """Кнопка с анимацией и хоккейным стилем."""
    bg_color = ListProperty(ACCENT)
    pressed_state = BooleanProperty(False)

    def __init__(self, text='', color=None, on_press_cb=None, **kw):
        super().__init__(text=text, **kw)
        self.color = DARK
        self.font_size = sp(16)
        self.bold = True
        if color: self.bg_color = color
        self._cb = on_press_cb
        self.bind(pos=self.redraw, size=self.redraw, bg_color=self.redraw)
        Clock.schedule_once(self.redraw, 0)

    def redraw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            col = self.bg_color
            if self.pressed_state:
                col = [c * 0.7 for c in col[:3]] + [col[3]]
            Color(*col)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])

    def on_press(self):
        self.pressed_state = True
        self.redraw()
        if self._cb: self._cb()

    def on_release(self):
        self.pressed_state = False
        self.redraw()


class StatCard(BoxLayout):
    def __init__(self, title='', value='', accent=None, **kw):
        super().__init__(orientation='vertical', size_hint_y=None, height=dp(90),
                         padding=dp(10), spacing=dp(2), **kw)
        accent = accent or ACCENT
        with self.canvas.before:
            Color(*PANEL)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            Color(*accent)
            self._stripe = Rectangle(pos=(self.x, self.y + self.height - dp(4)),
                                      size=(self.width, dp(4)))
        self.bind(pos=self._upd, size=self._upd)
        lbl_title = Label(text=title, color=MUTED, font_size=sp(11), bold=True,
                          size_hint_y=0.4, halign='center')
        self.add_widget(lbl_title)
        self.val_lbl = Label(text=value, color=accent, font_size=sp(22), bold=True,
                              size_hint_y=0.6)
        self.add_widget(self.val_lbl)

    def _upd(self, *a):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._stripe.pos = (self.x, self.y + self.height - dp(4))
        self._stripe.size = (self.width, dp(4))


class TeamCard(ButtonBehavior, BoxLayout):
    def __init__(self, team, on_select=None, **kw):
        super().__init__(orientation='horizontal', size_hint_y=None, height=dp(64),
                          padding=dp(6), spacing=dp(8), **kw)
        self.team = team
        self._cb = on_select
        with self.canvas.before:
            Color(*PANEL)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            Color(*ACCENT)
            self._stripe = Rectangle(pos=(self.x, self.y), size=(dp(4), self.height))
        self.bind(pos=self._upd, size=self._upd)
        logo = LogoWidget(color1=team.color1, color2=team.color2, abbr=team.abbr,
                           size_hint=(None, 1), width=dp(52))
        self.add_widget(logo)
        info = BoxLayout(orientation='vertical', size_hint_x=1)
        name_lbl = Label(text=f"{team.name}", color=WHITE, font_size=sp(14), bold=True,
                          halign='left', valign='middle')
        name_lbl.bind(size=lambda s, v: setattr(s, 'text_size', v))
        info.add_widget(name_lbl)
        city_lbl = Label(text=team.city, color=MUTED, font_size=sp(10),
                          halign='left', valign='middle', size_hint_y=0.6)
        city_lbl.bind(size=lambda s, v: setattr(s, 'text_size', v))
        info.add_widget(city_lbl)
        self.add_widget(info)
        stat = Label(text=f"{int((team.base_attack + team.base_defense) / 2)}",
                      color=GOLD, font_size=sp(16), bold=True, size_hint_x=None, width=dp(44))
        self.add_widget(stat)

    def _upd(self, *a):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._stripe.pos = (self.x, self.y)
        self._stripe.size = (dp(4), self.height)

    def on_release(self):
        if self._cb: self._cb(self.team)


# ==================== ЭКРАНЫ ====================
class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.build_ui()

    def build_ui(self):
        layout = FloatLayout()
        with layout.canvas.before:
            Color(*BG)
            self._bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda *a: setattr(self._bg, 'pos', layout.pos),
                    size=lambda *a: setattr(self._bg, 'size', layout.size))

        title = Label(text='[b]HOCKEY[/b]\nMANAGER', markup=True,
                       color=WHITE, font_size=sp(46), bold=True,
                       pos_hint={'center_x': 0.5, 'top': 0.95}, size_hint=(1, 0.15))
        layout.add_widget(title)

        # Декоративная линия
        line = Widget(size_hint=(0.7, None), height=dp(2),
                       pos_hint={'center_x': 0.5, 'top': 0.78})
        with line.canvas:
            Color(*ACCENT)
            Rectangle(pos=line.pos, size=line.size)
        line.bind(pos=lambda *a: self._redraw_line(line),
                  size=lambda *a: self._redraw_line(line))
        layout.add_widget(line)

        # Шайба
        puck = PuckWidget(size_hint=(None, None), size=(dp(220), dp(220)),
                           pos_hint={'center_x': 0.5, 'center_y': 0.55})
        layout.add_widget(puck)

        # Кнопки
        btn1 = HockeyButton(text='▶  НОВАЯ ИГРА', color=ACCENT,
                             size_hint=(0.7, None), height=dp(58),
                             pos_hint={'center_x': 0.5, 'center_y': 0.25},
                             on_press_cb=self.new_game)
        layout.add_widget(btn1)

        btn2 = HockeyButton(text='📂  ЗАГРУЗИТЬ', color=PANEL2,
                             size_hint=(0.7, None), height=dp(54),
                             pos_hint={'center_x': 0.5, 'center_y': 0.16},
                             on_press_cb=self.load_game)
        layout.add_widget(btn2)

        # Подпись
        foot = Label(text='BUILD 1.0  •  Hockey Manager',
                      color=MUTED, font_size=sp(10),
                      pos_hint={'center_x': 0.5, 'y': 0.02}, size_hint=(1, 0.05))
        layout.add_widget(foot)

        # Пульсация кнопки
        Animation(opacity=1.0, duration=1).start(btn1)
        def pulse(dt):
            a = Animation(opacity=0.75, duration=0.8) + Animation(opacity=1, duration=0.8)
            a.repeat = True
            a.start(btn1)
        Clock.schedule_once(pulse, 1)

        self.add_widget(layout)

    def _redraw_line(self, w):
        w.canvas.clear()
        with w.canvas:
            Color(*ACCENT)
            Rectangle(pos=w.pos, size=w.size)

    def new_game(self):
        self.manager.transition = SlideTransition(direction='left', duration=0.35)
        self.manager.current = 'league'

    def load_game(self):
        popup = Popup(title='Загрузка', title_color=WHITE, title_size=sp(16),
                       separator_color=ACCENT,
                       content=Label(text='Сохранения появятся позже',
                                     color=TEXT),
                       size_hint=(0.8, 0.3), background_color=PANEL)
        popup.open()


class LeagueScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(10))
        with root.canvas.before:
            Color(*BG)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, 'pos', root.pos),
                  size=lambda *a: setattr(self._bg, 'size', root.size))

        header = Label(text='🏆 ВЫБЕРИТЕ ЛИГУ', color=WHITE, font_size=sp(22),
                        bold=True, size_hint_y=None, height=dp(50))
        root.add_widget(header)

        scroll = ScrollView(size_hint=(1, 1))
        grid = BoxLayout(orientation='vertical', spacing=dp(12),
                          size_hint_y=None, padding=dp(6))
        grid.bind(minimum_height=grid.setter('height'))

        for key, L in LEAGUES.items():
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150),
                              padding=dp(12), spacing=dp(6))
            with card.canvas.before:
                Color(*PANEL)
                bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(14)])
                Color(*ACCENT)
                top = Rectangle(pos=(card.x, card.y + card.height - dp(4)),
                                 size=(card.width, dp(4)))
            card.bind(pos=lambda *a, b=bg, t=top, c=card: (
                setattr(b, 'pos', c.pos), setattr(b, 'size', c.size),
                setattr(t, 'pos', (c.x, c.y + c.height - dp(4))),
                setattr(t, 'size', (c.width, dp(4))))
            title_lbl = Label(text=f"[b]{L['name']}[/b]", markup=True, color=WHITE,
                               font_size=sp(28), size_hint_y=0.5)
            card.add_widget(title_lbl)
            info_lbl = Label(text=f"{len(L['teams'])} команд  •  {L['matches']} матчей  •  {L['cup']}",
                              color=ICE, font_size=sp(12), size_hint_y=0.3)
            card.add_widget(info_lbl)
            pick = HockeyButton(text='ВЫБРАТЬ', color=ACCENT, size_hint_y=0.4,
                                 on_press_cb=lambda k=key: self.pick(k))
            card.add_widget(pick)
            grid.add_widget(card)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        back = HockeyButton(text='← НАЗАД', color=PANEL2, size_hint_y=None,
                             height=dp(50), on_press_cb=self.go_back)
        root.add_widget(back)

        self.add_widget(root)

    def pick(self, key):
        self.manager.get_screen('team').set_league(key)
        self.manager.transition = SlideTransition(direction='left', duration=0.35)
        self.manager.current = 'team'

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.35)
        self.manager.current = 'menu'


class TeamScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.league_key = 'KHL'
        self.root_layout = None

    def set_league(self, key):
        self.league_key = key
        self.build_ui()

    def build_ui(self):
        if self.root_layout:
            self.remove_widget(self.root_layout)
        L = LEAGUES[self.league_key]
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
        with root.canvas.before:
            Color(*BG)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, 'pos', root.pos),
                  size=lambda *a: setattr(self._bg, 'size', root.size))

        header = Label(text=f'🏒 {L["name"]} — команда', color=WHITE,
                        font_size=sp(18), bold=True, size_hint_y=None, height=dp(44))
        root.add_widget(header)

        scroll = ScrollView(size_hint=(1, 1))
        grid = BoxLayout(orientation='vertical', spacing=dp(6),
                          size_hint_y=None, padding=dp(4))
        grid.bind(minimum_height=grid.setter('height'))

        for idx, d in enumerate(L['teams']):
            team = Team(d, is_user=False)
            card = TeamCard(team, on_select=lambda t, i=idx: self.pick(i))
            grid.add_widget(card)

        scroll.add_widget(grid)
        root.add_widget(scroll)

        back = HockeyButton(text='← НАЗАД', color=PANEL2, size_hint_y=None,
                             height=dp(50), on_press_cb=self.go_back)
        root.add_widget(back)

        self.root_layout = root
        self.add_widget(root)

    def pick(self, idx):
        game = Game(self.league_key, idx)
        self.manager.get_screen('game').start_game(game)
        self.manager.transition = FadeTransition(duration=0.5)
        self.manager.current = 'game'

    def go_back(self):
        self.manager.transition = SlideTransition(direction='right', duration=0.35)
        self.manager.current = 'league'


class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.game = None
        self.current_tab = 'dash'
        self.content_area = None
        self.header_label = None
        self.logo_container = None
        self.tab_buttons = {}

    def start_game(self, game):
        self.game = game
        self.build_ui()

    def build_ui(self):
        # Очищаем
        self.clear_widgets()
        root = BoxLayout(orientation='vertical')
        with root.canvas.before:
            Color(*BG)
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(self._bg, 'pos', root.pos),
                  size=lambda *a: setattr(self._bg, 'size', root.size))

        # HEADER
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(72),
                            padding=dp(8), spacing=dp(8))
        with header.canvas.before:
            Color(*PANEL)
            hbg = Rectangle(pos=header.pos, size=header.size)
            Color(*ACCENT)
            hstripe = Rectangle(pos=(header.x, header.y), size=(header.width, dp(3)))
        header.bind(pos=lambda *a, b=hbg, s=hstripe, h=header: (
            setattr(b, 'pos', h.pos), setattr(b, 'size', h.size),
            setattr(s, 'pos', (h.x, h.y)), setattr(s, 'size', (h.width, dp(3)))))

        logo_cont = BoxLayout(size_hint_x=None, width=dp(56))
        logo = LogoWidget(color1=self.game.user.color1, color2=self.game.user.color2,
                           abbr=self.game.user.abbr, size_hint=(1, 1))
        logo_cont.add_widget(logo)
        header.add_widget(logo_cont)

        info = BoxLayout(orientation='vertical')
        name_lbl = Label(text=f'[b]{self.game.user.name}[/b]', markup=True,
                          color=WHITE, font_size=sp(15), halign='left', valign='middle')
        name_lbl.bind(size=lambda s, v: setattr(s, 'text_size', v))
        info.add_widget(name_lbl)
        self.sub_label = Label(text=self._sub_text(), color=MUTED, font_size=sp(10),
                                halign='left', valign='middle')
        self.sub_label.bind(size=lambda s, v: setattr(s, 'text_size', v))
        info.add_widget(self.sub_label)
        header.add_widget(info)

        root.add_widget(header)

        # CONTENT
        self.content_area = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(6))
        root.add_widget(self.content_area)

        # TABS
        tabs = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(58),
                          spacing=dp(2))
        tab_defs = [('dash','🏠','Главная'), ('roster','👥','Состав'),
                    ('calendar','📅','Календарь'), ('table','📊','Таблица'),
                    ('playoff','🏆','Плей-офф')]
        for key, icon, name in tab_defs:
            b = HockeyButton(text=f'{icon}\n{name}', color=PANEL,
                              on_press_cb=lambda k=key: self.switch_tab(k))
            self.tab_buttons[key] = b
            tabs.add_widget(b)
        root.add_widget(tabs)

        self.add_widget(root)
        self.switch_tab('dash')

    def _sub_text(self):
        u = self.game.user
        return f'{LEAGUES[self.game.league_key]["name"]}  •  Очки: {u.points}  •  День: {self.game.day}/240'

    def switch_tab(self, key):
        self.current_tab = key
        for k, b in self.tab_buttons.items():
            b.bg_color = ACCENT if k == key else PANEL
            b.redraw()
        self.refresh_content()

    def refresh_content(self):
        self.content_area.clear_widgets()
        if self.current_tab == 'dash':
            self._content_dashboard()
        elif self.current_tab == 'roster':
            self._content_roster()
        elif self.current_tab == 'calendar':
            self._content_calendar()
        elif self.current_tab == 'table':
            self._content_table()
        elif self.current_tab == 'playoff':
            self._content_playoff()
        # обновляем шапку
        if hasattr(self, 'sub_label'):
            self.sub_label.text = self._sub_text()

    def _content_dashboard(self):
        u = self.game.user
        # Кнопка "ДАЛЕЕ"
        ctrl = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(6))
        next_btn = HockeyButton(text='⏩ ДЕНЬ ВПЕРЁД', color=GREEN,
                                 on_press_cb=self.advance_day)
        ctrl.add_widget(next_btn)
        auto_btn = HockeyButton(text='⚡ СЕЗОН', color=ACCENT2,
                                 on_press_cb=self.sim_season)
        ctrl.add_widget(auto_btn)
        self.content_area.add_widget(ctrl)

        # Статы
        stats_grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(280))
        stats_grid.add_widget(StatCard(title='ДОВЕРИЕ', value=f'{u.trust}%', accent=ICE))
        stats_grid.add_widget(StatCard(title='ОЧКИ', value=str(u.points), accent=ACCENT))
        stats_grid.add_widget(StatCard(title='ПОБЕДЫ', value=str(u.wins), accent=GREEN))
        stats_grid.add_widget(StatCard(title='ПОРАЖЕНИЯ', value=str(u.losses), accent=RED))
        stats_grid.add_widget(StatCard(title='ГОЛЫ', value=f'{u.gf}:{u.ga}', accent=GOLD))
        stats_grid.add_widget(StatCard(title='ДЕНЬ', value=f'{self.game.day}', accent=MUTED))
        self.content_area.add_widget(stats_grid)

        # Следующий матч
        next_lbl = Label(text='СЛЕДУЮЩИЙ МАТЧ', color=ACCENT, font_size=sp(12),
                          bold=True, size_hint_y=None, height=dp(24))
        self.content_area.add_widget(next_lbl)

        # Ищем следующий матч юзера
        next_match = None
        for i in range(self.game.day, len(self.game.calendar)):
            for a, b in self.game.calendar[i]:
                if a == self.game.user_idx or b == self.game.user_idx:
                    next_match = (i, a, b)
                    break
            if next_match: break

        if next_match:
            i, a, b = next_match
            ha = self.game.teams[a]; aw = self.game.teams[b]
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80),
                              padding=dp(8), spacing=dp(6))
            with card.canvas.before:
                Color(*PANEL)
                RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
            card.bind(pos=lambda *a, c=card: self._redraw_bg(c))
            card.bind(size=lambda *a, c=card: self._redraw_bg(c))
            lg1 = LogoWidget(color1=ha.color1, color2=ha.color2, abbr=ha.abbr,
                              size_hint=(None, 1), width=dp(56))
            card.add_widget(lg1)
            vs = Label(text='VS', color=ACCENT2, font_size=sp(20), bold=True,
                        size_hint_x=0.3)
            card.add_widget(vs)
            lg2 = LogoWidget(color1=aw.color1, color2=aw.color2, abbr=aw.abbr,
                              size_hint=(None, 1), width=dp(56))
            card.add_widget(lg2)
            self.content_area.add_widget(card)

            play = HockeyButton(text='▶ ИГРАТЬ МАТЧ', color=GREEN, size_hint_y=None,
                                 height=dp(52),
                                 on_press_cb=lambda h=a, aw=b: self.play_match(h, aw))
            self.content_area.add_widget(play)

    def _redraw_bg(self, c):
        c.canvas.before.clear()
        with c.canvas.before:
            Color(*PANEL)
            RoundedRectangle(pos=c.pos, size=c.size, radius=[dp(10)])

    def _content_roster(self):
        header = Label(text='👥 СОСТАВ', color=WHITE, font_size=sp(18),
                        bold=True, size_hint_y=None, height=dp(30))
        self.content_area.add_widget(header)
        scroll = ScrollView()
        grid = BoxLayout(orientation='vertical', spacing=dp(4),
                          size_hint_y=None, padding=dp(2))
        grid.bind(minimum_height=grid.setter('height'))
        for p in sorted(self.game.user.players, key=lambda x: (x.pos, -x.skill)):
            row = BoxLayout(size_hint_y=None, height=dp(48), padding=dp(6), spacing=dp(6))
            with row.canvas.before:
                Color(*PANEL)
                RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(8)])
            row.bind(pos=lambda *a, r=row: self._redraw_row(r))
            row.bind(size=lambda *a, r=row: self._redraw_row(r))
            pos_color = {'G': GOLD, 'D': ACCENT, 'F': GREEN}.get(p.pos, WHITE)
            row.add_widget(Label(text=p.pos, color=pos_color, font_size=sp(14),
                                  bold=True, size_hint_x=None, width=dp(30)))
            name = Label(text=p.name, color=TEXT, font_size=sp(12),
                          halign='left', valign='middle')
            name.bind(size=lambda s, v: setattr(s, 'text_size', v))
            row.add_widget(name)
            row.add_widget(Label(text=str(p.skill), color=GOLD, font_size=sp(14),
                                  bold=True, size_hint_x=None, width=dp(40)))
            row.add_widget(Label(text=f'{p.age}', color=MUTED, font_size=sp(11),
                                  size_hint_x=None, width=dp(30)))
            grid.add_widget(row)
        scroll.add_widget(grid)
        self.content_area.add_widget(scroll)

    def _redraw_row(self, r):
        r.canvas.before.clear()
        with r.canvas.before:
            Color(*PANEL)
            RoundedRectangle(pos=r.pos, size=r.size, radius=[dp(8)])

    def _content_calendar(self):
        header = Label(text='📅 КАЛЕНДАРЬ', color=WHITE, font_size=sp(18),
                        bold=True, size_hint_y=None, height=dp(30))
        self.content_area.add_widget(header)
        scroll = ScrollView()
        grid = BoxLayout(orientation='vertical', spacing=dp(3),
                          size_hint_y=None, padding=dp(2))
        grid.bind(minimum_height=grid.setter('height'))
        shown = 0
        for i in range(self.game.day, len(self.game.calendar)):
            for a, b in self.game.calendar[i]:
                is_user = (a == self.game.user_idx or b == self.game.user_idx)
                row = BoxLayout(size_hint_y=None, height=dp(40), padding=dp(6))
                with row.canvas.before:
                    Color(*PANEL2 if is_user else PANEL)
                    RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(6)])
                row.bind(pos=lambda *a, r=row: self._redraw_row2(r))
                row.bind(size=lambda *a, r=row: self._redraw_row2(r))
                ha = self.game.teams[a]; aw = self.game.teams[b]
                txt = f'Д{i+1}: {ha.name} — {aw.name}'
                lbl = Label(text=txt, color=TEXT if is_user else MUTED,
                             font_size=sp(11), halign='left', valign='middle')
                lbl.bind(size=lambda s, v: setattr(s, 'text_size', v))
                row.add_widget(lbl)
                grid.add_widget(row)
                shown += 1
                if shown > 100: break
            if shown > 100: break
        scroll.add_widget(grid)
        self.content_area.add_widget(scroll)

    def _redraw_row2(self, r):
        r.canvas.before.clear()
        with r.canvas.before:
            # цвет определяем по первому ребенку
            lbl = r.children[0] if r.children else None
            col = PANEL2 if (lbl and lbl.color == TEXT) else PANEL
            Color(*PANEL)
            RoundedRectangle(pos=r.pos, size=r.size, radius=[dp(6)])

    def _content_table(self):
        header = Label(text='📊 ТАБЛИЦА', color=WHITE, font_size=sp(18),
                        bold=True, size_hint_y=None, height=dp(30))
        self.content_area.add_widget(header)
        scroll = ScrollView()
        grid = BoxLayout(orientation='vertical', spacing=dp(3),
                          size_hint_y=None, padding=dp(2))
        grid.bind(minimum_height=grid.setter('height'))
        # Заголовок
        hrow = BoxLayout(size_hint_y=None, height=dp(30), padding=dp(6))
        for txt, w in [('#', 0.1), ('Команда', 0.45), ('И', 0.1), ('О', 0.15), ('Ш', 0.2)]:
            hrow.add_widget(Label(text=txt, color=ACCENT, font_size=sp(11), bold=True,
                                    size_hint_x=w))
        grid.add_widget(hrow)

        for pos, team in enumerate(self.game.standings(), 1):
            row = BoxLayout(size_hint_y=None, height=dp(42), padding=dp(6))
            with row.canvas.before:
                Color(*ACCENT2 if team.is_user else PANEL)
                RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(6)])
            row.bind(pos=lambda *a, r=row: self._redraw_row3(r),
                      size=lambda *a, r=row: self._redraw_row3(r))
            row.add_widget(Label(text=str(pos), color=TEXT, font_size=sp(12),
                                  size_hint_x=0.1, bold=True))
            name = Label(text=team.name, color=WHITE, font_size=sp(12),
                          halign='left', valign='middle', size_hint_x=0.45)
            name.bind(size=lambda s, v: setattr(s, 'text_size', v))
            row.add_widget(name)
            row.add_widget(Label(text=f'{team.wins+team.losses}', color=MUTED,
                                  font_size=sp(11), size_hint_x=0.1))
            row.add_widget(Label(text=str(team.points), color=GOLD, font_size=sp(13),
                                  bold=True, size_hint_x=0.15))
            row.add_widget(Label(text=f'{team.gf}:{team.ga}', color=ICE,
                                  font_size=sp(11), size_hint_x=0.2))
            grid.add_widget(row)
        scroll.add_widget(grid)
        self.content_area.add_widget(scroll)

    def _redraw_row3(self, r):
        r.canvas.before.clear()
        with r.canvas.before:
            Color(*PANEL)
            RoundedRectangle(pos=r.pos, size=r.size, radius=[dp(6)])

    def _content_playoff(self):
        header = Label(text='🏆 ПЛЕЙ-ОФФ', color=WHITE, font_size=sp(18),
                        bold=True, size_hint_y=None, height=dp(30))
        self.content_area.add_widget(header)

        g = self.game
        if not g.playoff_stage:
            msg = Label(text=f"Регулярка идёт\nДень {g.day} из {len(g.calendar)}",
                         color=MUTED, font_size=sp(13), halign='center')
            self.content_area.add_widget(msg)
            btn = HockeyButton(text='⏩ СИМУЛИРОВАТЬ СЕЗОН', color=ACCENT2,
                                size_hint_y=None, height=dp(60),
                                on_press_cb=self.sim_season)
            self.content_area.add_widget(btn)
            return

        if g.playoff_stage == 'done' and g.champion:
            trophy = Label(text=f'🏆\n\n{g.champion.name}\n\nОБЛАДАТЕЛЬ {LEAGUES[g.league_key]["cup"].upper()}',
                            color=GOLD, font_size=sp(16), bold=True, halign='center')
            self.content_area.add_widget(trophy)
            btn = HockeyButton(text='🎉 НОВЫЙ СЕЗОН', color=GREEN,
                                size_hint_y=None, height=dp(56),
                                on_press_cb=self.new_season)
            self.content_area.add_widget(btn)
            return

        sim_btn = HockeyButton(text='⏩ СИМУЛИРОВАТЬ СТАДИЮ', color=ACCENT2,
                                size_hint_y=None, height=dp(50),
                                on_press_cb=self.sim_playoff)
        self.content_area.add_widget(sim_btn)

        scroll = ScrollView()
        grid = BoxLayout(orientation='vertical', spacing=dp(4),
                          size_hint_y=None, padding=dp(2))
        grid.bind(minimum_height=grid.setter('height'))
        for conf, data in g.playoff_bracket.items():
            conf_lbl = Label(text=f'{conf} — {data["stage"]}', color=ACCENT,
                              font_size=sp(14), bold=True,
                              size_hint_y=None, height=dp(28))
            grid.add_widget(conf_lbl)
            for s in data['series']:
                a = g.teams[s['a']]; b = g.teams[s['b']]
                done = s['wins_a'] == 4 or s['wins_b'] == 4
                row = BoxLayout(size_hint_y=None, height=dp(46), padding=dp(6))
                with row.canvas.before:
                    Color(*PANEL)
                    RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(6)])
                row.bind(pos=lambda *a, r=row: self._redraw_row3(r),
                          size=lambda *a, r=row: self._redraw_row3(r))
                lbl = Label(text=f'{a.abbr}  {s["wins_a"]} : {s["wins_b"]}  {b.abbr}',
                             color=GREEN if done else TEXT, font_size=sp(12), bold=done)
                row.add_widget(lbl)
                grid.add_widget(row)
        scroll.add_widget(grid)
        self.content_area.add_widget(scroll)

    # ---- Действия ----
    def advance_day(self):
        r = self.game.next_day()
        if r.get('done'):
            self.game.start_playoffs()
            self.popup('Регулярка завершена!', 'Начинается плей-офф')
            self.refresh_content()
            return
        if r.get('user_pending'):
            a, b = r['user_pending']
            self.play_match(a, b)
        else:
            self.popup('День прошёл', f'Симулировано {len(r.get("results", []))} матчей')
        self.refresh_content()

    def play_match(self, home_id, away_id):
        sim = self.game.user_play_match(home_id, away_id)
        # Показываем результат
        title = 'Победа!' if (sim.hs > sim.aws and home_id == self.game.user_idx) or \
                              (sim.aws > sim.hs and away_id == self.game.user_idx) else \
                'Ничья' if sim.hs == sim.aws else 'Поражение'
        text = f'{sim.home.name}  {sim.hs} : {sim.aws}  {sim.away.name}\n\n{title}'
        self.popup(title, text)
        self.refresh_content()

    def sim_season(self):
        guard = 0
        while self.game.day < len(self.game.calendar) and guard < 600:
            guard += 1
            r = self.game.next_day()
            if r.get('done'): break
            if r.get('user_pending'):
                a, b = r['user_pending']
                self.game.user_play_match(a, b)
        if not self.game.playoff_stage:
            self.game.start_playoffs()
        self.popup('Сезон', 'Регулярка завершена')
        self.refresh_content()

    def sim_playoff(self):
        self.game.sim_playoff_stage()
        if self.game.playoff_stage == 'done':
            self.popup('🏆', f'Обладатель: {self.game.champion.name}')
        self.refresh_content()

    def new_season(self):
        # Просто сбрасываем и начинаем заново
        from kivy.uix.popup import Popup
        self.manager.transition = FadeTransition(duration=0.5)
        self.manager.current = 'menu'

    def popup(self, title, text):
        content = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))
        lbl = Label(text=text, color=TEXT, font_size=sp(13), halign='center')
        content.add_widget(lbl)
        close = HockeyButton(text='OK', color=ACCENT, size_hint_y=None, height=dp(50))
        content.add_widget(close)
        popup = Popup(title=title, title_color=WHITE, title_size=sp(15),
                       separator_color=ACCENT, content=content,
                       size_hint=(0.85, 0.4), background_color=PANEL)
        close._cb = popup.dismiss
        popup.open()


# ==================== APP ====================
class HockeyManagerApp(App):
    def build(self):
        self.title = 'Hockey Manager'
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LeagueScreen(name='league'))
        sm.add_widget(TeamScreen(name='team'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    HockeyManagerApp().run()
