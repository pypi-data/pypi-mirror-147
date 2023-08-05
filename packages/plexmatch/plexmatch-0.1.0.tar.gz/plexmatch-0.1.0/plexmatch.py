# -*- coding: utf-8 -*-
#
# Copyright (c) 2022~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import os
import re
from dataclasses import dataclass, field

_re_episode_id = re.compile(r'^(?:S(?P<season>\d+))?(?:E(?P<episode>\d+))$', re.I)

@dataclass
class EpisodeId:
    episode:    int
    season:     Optional[int] = None

    def tostr(self, *, ctx_season: Optional[int]=None) -> str:
        if self.season is None or self.season == ctx_season:
            return f'E{self.episode:02d}'
        else:
            return f'S{self.season:02d}E{self.episode:02d}'

    @classmethod
    def parse(cls, s: str) -> 'EpisodeId':
        m = _re_episode_id.match(s)
        if m is None:
            raise ValueError(f'invalid episode id: {s}')
        episode = int(m.group('episode'))
        season_str = m.group('season')
        season = int(season_str) if season_str else None
        return cls(episode=episode, season=season)


@dataclass
class EpisodeFile:
    name:   str
    start:  EpisodeId
    end:    Optional[EpisodeId] = None

    def tostr(self, *, ctx_season: Optional[int]=None) -> str:
        if self.end is None or self.start == self.end:
            prefix = self.start.tostr(ctx_season=ctx_season)

        else:
            end_ctx_season = ctx_season if self.start.season is None else self.start.season
            prefix = self.start.tostr(ctx_season=ctx_season) + \
                    '-' + self.end.tostr(ctx_season=end_ctx_season)
        return f'{prefix}: {self.name}'

    @classmethod
    def parse(cls, s: str) -> 'EpisodeFile':
        header, _, name = s.partition(':')
        start_str, _, end_str = header.partition('-')
        start = EpisodeId.parse(start_str)
        end = EpisodeId.parse(end_str) if end_str else None
        return cls(name=name.strip(), start=start, end=end)


@dataclass
class PlexMatch:
    show:       Optional[str] = None
    season:     Optional[int] = None
    episodes:   List[EpisodeFile] = field(default_factory=list)
    year:       Optional[int] = None
    tvdbid:     Optional[str] = None
    tmdbid:     Optional[str] = None
    imdbid:     Optional[str] = None
    guid:       Optional[str] = None

    def add_episode(self, name: str,
            episode_start: int, season_start: Optional[int] = None,
            episode_end: Optional[int]=None, season_end: Optional[int] = None) -> EpisodeFile:

        ef: EpisodeFile = EpisodeFile(name, EpisodeId(episode_start, season_start))
        if episode_end is not None:
            ef.end = EpisodeId(episode_end, season_end)
        self.episodes.append(ef)
        return ef


def tostr(
        plex_match: PlexMatch, *,
        linesep: str = os.linesep,
        prefer_title=False,
        prefer_episode=True,
        sort_episodes=False,
    ):
    lines = []

    if plex_match.guid is not None:
        lines.append(f'guid: {plex_match.guid}')

    if plex_match.show is not None:
        header = 'title' if prefer_title else 'show'
        lines.append(f'{header}: {plex_match.show}')

    if plex_match.season is not None:
        lines.append(f'season: {plex_match.season}')

    for id_name in ('tvdbid', 'tmdbid', 'imdbid'):
        id_value = getattr(plex_match, id_name)
        if id_value is not None:
            lines.append(f'{id_name}: {id_value}')

    if plex_match.year is not None:
        lines.append(f'year: {plex_match.year}')

    episodes = plex_match.episodes
    if sort_episodes:
        season_selector = (
            lambda s: s if s is not None else plex_match.season
        ) if isinstance(plex_match.season, int) else (
            lambda s: s
        )
        episodes = sorted(episodes, key=lambda ef: (season_selector(ef.start.season), ef.start.episode))

    if episodes:
        if len(set(e.start.season for e in episodes) | {None}) <= 2:
            ctx_season = plex_match.season
        else:
            ctx_season = None
        header = 'episode' if prefer_episode else 'ep'
        for episode in episodes:
            ep_str = episode.tostr(ctx_season=ctx_season)
            lines.append(f'{header}: {ep_str}')

    return linesep.join(lines)

_parse_mapping: Dict[str, Callable[[PlexMatch, str, str], None]] = {
    'show': lambda p, h, v: setattr(p, h, v),
    'season': lambda p, h, v: setattr(p, h, int(v)),
    'episode': lambda p, h, v: p.episodes.append(EpisodeFile.parse(v)),
}
# for same action (str)
_parse_mapping['tvdbid'] = _parse_mapping['tmdbid'] = _parse_mapping['show']
_parse_mapping['imdbid'] = _parse_mapping['guid'] = _parse_mapping['show']
# for same action (int)
_parse_mapping['year'] = _parse_mapping['season']
# for alias
_parse_mapping['title'] = _parse_mapping['show']
_parse_mapping['ep'] = _parse_mapping['episode']

def parse(s: str) -> PlexMatch:
    plex_match = PlexMatch()
    for line in s.splitlines():
        if line.strip():
            header, _, body = line.partition(':')
            header_w = header.lower().strip()
            if header_w not in _parse_mapping:
                raise ValueError(f'unknown header: {header}')
            _parse_mapping[header_w](plex_match, header_w, body.strip())
    return plex_match
