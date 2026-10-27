import asyncio
import aiohttp
import json
import re
import os
from datetime import datetime

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
RESET = "\033[0m"

SITES = {
    "Разработка": {
        "GitHub_API": "https://api.github.com/users/{u}", "GitLab_API": "https://gitlab.com/api/v4/users?username={u}",
        "PyPI_API": "https://pypi.org/pypi/{u}/json", "NPM_API": "https://registry.npmjs.org/~{u}",
        "DockerHub_API": "https://hub.docker.com/v2/users/{u}/", "Keybase_API": "https://keybase.io/_/api/1.0/user/lookup.json?username={u}",
        "HackerNews_API": "https://hacker-news.firebaseio.com/v0/user/{u}.json", "Reddit_API": "https://www.reddit.com/user/{u}/about.json",
        "Codeberg": "https://codeberg.org/{u}", "Gitea": "https://gitea.com/{u}", 
        "Replit": "https://replit.com/@{u}", "StackOverflow": "https://stackoverflow.com/users/{u}", 
        "Bitbucket": "https://bitbucket.org/{u}/", "SourceForge": "https://sourceforge.net/u/{u}/profile",
        "Kaggle": "https://www.kaggle.com/{u}", "Gravatar": "https://gravatar.com/{u}",
        "DevTo": "https://dev.to/{u}", "Hashnode": "https://hashnode.com/@{u}", "Codepen": "https://codepen.io/{u}",
        "Codesandbox": "https://codesandbox.io/u/{u}", "Glitch": "https://{u}.glitch.me", "Surge": "https://{u}.surge.sh",
        "HackerRank": "https://www.hackerrank.com/{u}", "LeetCode": "https://leetcode.com/{u}", "Codeforces": "https://codeforces.com/profile/{u}",
        "Codewars": "https://www.codewars.com/users/{u}", "Topcoder": "https://www.topcoder.com/members/{u}", "Hackaday": "https://hackaday.io/{u}",
        "Instructables": "https://www.instructables.com/member/{u}", "Thingiverse": "https://www.thingiverse.com/{u}", "Printables": "https://www.printables.com/social/{u}",
        "Cults3D": "https://cults3d.com/en/users/{u}", "Hackster": "https://www.hackster.io/{u}", "Hackernoon": "https://hackernoon.com/u/{u}",
        "FreeCodeCamp": "https://www.freecodecamp.org/{u}", "Wakatime": "https://wakatime.com/@{u}", "ProductHunt": "https://www.producthunt.com/@{u}",
        "IndieHackers": "https://www.indiehackers.com/{u}", "Lobsters": "https://lobste.rs/u/{u}", "Snyk": "https://snyk.io/@{u}",
        "Vercel": "https://vercel.com/{u}", "Netlify": "https://app.netlify.com/teams/{u}", "Heroku": "https://dashboard.heroku.com/{u}",
        "DigitalOcean": "https://cloud.digitalocean.com/account/{u}", "GoogleCloud": "https://console.cloud.google.com/{u}",
        "Gitbook": "https://{u}.gitbook.io", "Notion": "https://{u}.notion.site", "Carrd": "https://{u}.carrd.co", 
        "Figma": "https://www.figma.com/@{u}", "StackShare": "https://stackshare.io/{u}", "Devpost": "https://devpost.com/{u}", 
        "CodeSignal": "https://app.codesignal.com/profile/{u}", "Coderbyte": "https://coderbyte.com/profile/{u}", "Exercism": "https://exercism.org/profiles/{u}", 
        "Scrimba": "https://scrimba.com/@{u}", "HackerEarth": "https://www.hackerearth.com/@{u}", "Spoj": "https://www.spoj.com/users/{u}", 
        "Kattis": "https://open.kattis.com/users/{u}", "CodinGame": "https://www.codingame.com/profile/{u}", "Edabit": "https://edabit.com/user/{u}", 
        "CodeChef": "https://www.codechef.com/users/{u}", "Habr": "https://habr.com/ru/users/{u}/", "Tproger": "https://tproger.ru/user/{u}", 
        "DTF": "https://dtf.ru/u/{u}", "4PDA": "https://4pda.to/forum/index.php?showuser={u}", "SberCloud": "https://sbercloud.ru/{u}", 
        "YandexCloud": "https://yandex.cloud/ru/users/{u}", "GitMemory": "https://gitmemory.com/{u}", "Coder": "https://coder.com/{u}",
        "Devrant": "https://devrant.com/users/{u}", "CodeProject": "https://www.codeproject.com/Members/{u}", "Gitee": "https://gitee.com/{u}",
        "Bitbucket_API": "https://api.bitbucket.org/2.0/users/{u}"
    },
    "Соцсети и блоги": {
        "Telegram": "https://t.me/{u}", "VK": "https://vk.com/{u}", "OK": "https://ok.ru/{u}",
        "Pinterest": "https://www.pinterest.com/{u}/", "Tumblr": "https://{u}.tumblr.com", 
        "Medium": "https://medium.com/@{u}", "Quora": "https://www.quora.com/profile/{u}",
        "Goodreads": "https://www.goodreads.com/{u}", "Letterboxd": "https://letterboxd.com/{u}/", "Wattpad": "https://www.wattpad.com/user/{u}",
        "LiveJournal": "https://{u}.livejournal.com", "Diary": "https://{u}.diary.ru", "Dreamwidth": "https://{u}.dreamwidth.org",
        "Plurk": "https://www.plurk.com/{u}", "Hive": "https://hive.blog/@{u}", "Steemit": "https://steemit.com/@{u}",
        "WordPress": "https://{u}.wordpress.com", "Blogger": "https://{u}.blogspot.com", "Wix": "https://{u}.wixsite.com",
        "Weebly": "https://{u}.weebly.com", "Jimdo": "https://{u}.jimdosite.com", "Strikingly": "https://{u}.mystrikingly.com",
        "AboutMe": "https://about.me/{u}", "Linktree": "https://linktr.ee/{u}", "Beacons": "https://beacons.ai/{u}",
        "BioLink": "https://bio.link/{u}", "Campsite": "https://campsite.bio/{u}", "Taplink": "https://taplink.cc/{u}",
        "MyWorld": "https://my.mail.ru/{u}", "YandexZen": "https://zen.yandex.ru/{u}", "Pikabu": "https://pikabu.ru/@{u}",
        "Boosty": "https://boosty.to/{u}", "Mastodon": "https://mastodon.social/@{u}", "Bluesky": "https://bsky.app/profile/{u}.bsky.social",
        "Threads": "https://www.threads.net/@{u}", "Vero": "https://vero.co/{u}", "Minds": "https://www.minds.com/{u}",
        "MeWe": "https://mewe.com/i/{u}", "Parler": "https://parler.com/profile/{u}", "Gab": "https://gab.com/{u}",
        "Gettr": "https://gettr.com/user/{u}", "TruthSocial": "https://truthsocial.com/@{u}", "Rumble": "https://rumble.com/user/{u}",
        "Odysee": "https://odysee.com/@{u}", "BitChute": "https://www.bitchute.com/channel/{u}/", "Lbry": "https://lbry.tv/@{u}",
        "Substack": "https://{u}.substack.com", "Ghost": "https://{u}.ghost.io", "Bearblog": "https://{u}.bearblog.dev",
        "WriteAs": "https://write.as/{u}", "TelegraPh": "https://telegra.ph/{u}", "HackMD": "https://hackmd.io/@{u}",
        "Kinja": "https://{u}.kinja.com", "Svbtle": "https://{u}.svbtle.com", "PostachIo": "https://{u}.postach.io"
    },
    "Игры и стриминг": {
        "Steam": "https://steamcommunity.com/id/{u}", "Twitch": "https://www.twitch.tv/{u}", "EpicGames": "https://www.epicgames.com/id/{u}",
        "Xbox": "https://xboxgamertag.com/search/{u}", "PSN": "https://psnprofiles.com/{u}", "Roblox": "https://www.roblox.com/user.aspx?username={u}", 
        "Chess": "https://www.chess.com/member/{u}", "Lichess": "https://lichess.org/@{u}", "Faceit": "https://www.faceit.com/en/players/{u}", 
        "Osu": "https://osu.ppy.sh/users/{u}", "Speedrun": "https://www.speedrun.com/user/{u}", "BattleNet": "https://battle.net/{u}", 
        "GOG": "https://www.gog.com/u/{u}", "ItchIo": "https://{u}.itch.io", "Gamejolt": "https://gamejolt.com/@{u}", 
        "Kongregate": "https://www.kongregate.com/accounts/{u}", "Newgrounds": "https://{u}.newgrounds.com", "ArmorGames": "https://armorgames.com/user/{u}", 
        "Miniclip": "https://www.miniclip.com/user/{u}", "Poki": "https://poki.com/user/{u}", "CrazyGames": "https://www.crazygames.com/user/{u}", 
        "Y8": "https://www.y8.com/user/{u}", "AddictingGames": "https://www.addictinggames.com/user/{u}", "Twoplayergames": "https://www.twoplayergames.org/user/{u}", 
        "Silvergames": "https://www.silvergames.com/user/{u}", "Frive": "https://frive.net/user/{u}", "SteamDB": "https://steamdb.info/calculator/?player={u}", 
        "SteamCharts": "https://steamcharts.com/{u}", "SteamSpy": "https://steamspy.com/{u}", "Backloggd": "https://backloggd.com/u/{u}", 
        "HowLongToBeat": "https://howlongtobeat.com/user/{u}", "Grouvee": "https://www.grouvee.com/user/{u}", "IGDB": "https://www.igdb.com/{u}", 
        "Rawg": "https://rawg.io/@{u}", "Glitchwave": "https://glitchwave.com/user/{u}", "YouTube": "https://www.youtube.com/@{u}", 
        "Rutube": "https://rutube.ru/channel/{u}/", "Vimeo": "https://vimeo.com/{u}", "Veoh": "https://veoh.com/{u}", 
        "Metacafe": "https://metacafe.com/{u}", "BuzzFeed": "https://buzzfeed.com/{u}", "Mashable": "https://mashable.com/{u}", 
        "TechCrunch": "https://techcrunch.com/{u}", "TheVerge": "https://theverge.com/{u}", "Wired": "https://wired.com/{u}", 
        "ArsTechnica": "https://arstechnica.com/{u}", "Engadget": "https://engadget.com/{u}", "Gizmodo": "https://gizmodo.com/{u}", 
        "Lifehacker": "https://lifehacker.com/{u}", "Kotaku": "https://kotaku.com/{u}", "Polygon": "https://polygon.com/{u}", 
        "IGN": "https://ign.com/{u}", "GameSpot": "https://gamespot.com/{u}", "Eurogamer": "https://eurogamer.net/{u}", 
        "PCGamer": "https://pcgamer.com/{u}", "StopGame": "https://stopgame.ru/user/{u}", "Kanobu": "https://kanobu.ru/user/{u}", 
        "DTFGames": "https://dtf.ru/u/{u}", "VKPlay": "https://vkplay.ru/{u}", "Trovo": "https://trovo.live/s/{u}",
        "Dlive": "https://dlive.tv/{u}", "Caffeine": "https://www.caffeine.tv/{u}", "NimoTV": "https://www.nimo.tv/{u}",
        "AfreecaTV": "https://www.afreecatv.com/{u}", "Bigo": "https://www.bigo.tv/{u}", "Nonolive": "https://nonolive.com/{u}"
    },
    "Музыка и аудио": {
        "SoundCloud": "https://soundcloud.com/{u}", "Spotify": "https://open.spotify.com/user/{u}", "Bandcamp": "https://{u}.bandcamp.com",
        "Mixcloud": "https://www.mixcloud.com/{u}/", "LastFM": "https://www.last.fm/user/{u}", "Discogs": "https://www.discogs.com/user/{u}",
        "Audiomack": "https://audiomack.com/{u}", "ReverbNation": "https://www.reverbnation.com/{u}", "Deezer": "https://www.deezer.com/{u}",
        "Tidal": "https://tidal.com/@{u}", "AppleMusic": "https://music.apple.com/profile/{u}", "AmazonMusic": "https://music.amazon.com/{u}",
        "YouTubeMusic": "https://music.youtube.com/@{u}", "Pandora": "https://www.pandora.com/artist/{u}", "iHeartRadio": "https://www.iheart.com/artist/{u}",
        "TuneIn": "https://tunein.com/user/{u}", "Audible": "https://www.audible.com/{u}", "PodcastAddict": "https://podcastaddict.com/{u}",
        "Overcast": "https://overcast.fm/{u}", "Castro": "https://castro.fm/{u}", "PocketCasts": "https://pocketcasts.com/{u}",
        "Breaker": "https://breaker.audio/{u}", "Anchor": "https://anchor.fm/{u}", "Buzzsprout": "https://www.buzzsprout.com/{u}",
        "Libsyn": "https://{u}.libsyn.com", "Podbean": "https://{u}.podbean.com", "Spreaker": "https://www.spreaker.com/user/{u}",
        "Sounder": "https://sounder.fm/{u}", "Simplecast": "https://{u}.simplecast.com", "Transistor": "https://{u}.transistor.fm",
        "RedCircle": "https://redcircle.com/{u}", "Castbox": "https://castbox.fm/user/{u}", "Stitcher": "https://www.stitcher.com/{u}",
        "Podchaser": "https://www.podchaser.com/users/{u}", "ListenNotes": "https://www.listennotes.com/users/{u}", "PlayerFM": "https://player.fm/{u}",
        "PodcastRepublic": "https://www.podcastrepublic.net/{u}", "Podyssey": "https://podyssey.fm/{u}", "Goodpods": "https://goodpods.com/{u}",
        "Rephonic": "https://rephonic.com/u/{u}", "Chartable": "https://chartable.com/{u}", "Podtrac": "https://podtrac.com/{u}",
        "Blubrry": "https://blubrry.com/{u}", "Megaphone": "https://megaphone.fm/{u}", "Acast": "https://{u}.acast.com",
        "Omny": "https://omny.fm/shows/{u}", "Art19": "https://art19.com/shows/{u}", "Whooshkaa": "https://whooshkaa.com/{u}",
        "Genius": "https://genius.com/{u}", "Musixmatch": "https://www.musixmatch.com/profile/{u}", "Shazam": "https://www.shazam.com/user/{u}",
        "YandexMusic": "https://music.yandex.ru/users/{u}", "VKMusic": "https://vk.com/audio?performer={u}", "NTSRadio": "https://www.nts.live/u/{u}",
        "ResidentAdvisor": "https://www.residentadvisor.net/profile/{u}", "Beatport": "https://www.beatport.com/artist/{u}", "Traxsource": "https://www.traxsource.com/artist/{u}"
    },
    "Дизайн и фото": {
        "Behance": "https://www.behance.net/{u}", "Dribbble": "https://dribbble.com/{u}", "DeviantArt": "https://www.deviantart.com/{u}",
        "ArtStation": "https://www.artstation.com/{u}", "500px": "https://500px.com/p/{u}", "Unsplash": "https://unsplash.com/@{u}",
        "Pexels": "https://www.pexels.com/@{u}", "Pixabay": "https://pixabay.com/users/{u}/", "Figma": "https://www.figma.com/@{u}",
        "VSCO": "https://vsco.co/{u}", "Flickr": "https://www.flickr.com/people/{u}", "Shutterstock": "https://www.shutterstock.com/g/{u}",
        "iStock": "https://www.istockphoto.com/portfolio/{u}", "AdobeStock": "https://stock.adobe.com/contributor/{u}", "GettyImages": "https://www.gettyimages.com/photos/{u}",
        "Alamy": "https://www.alamy.com/stock-photo/{u}.html", "Dreamstime": "https://www.dreamstime.com/{u}_info", "Depositphotos": "https://depositphotos.com/portfolio-{u}.html",
        "Pond5": "https://www.pond5.com/artist/{u}", "Vecteezy": "https://www.vecteezy.com/members/{u}", "Freepik": "https://www.freepik.com/author/{u}",
        "Envato": "https://themeforest.net/user/{u}", "CreativeMarket": "https://creativemarket.com/{u}", "Gumroad": "https://{u}.gumroad.com",
        "Sellfy": "https://{u}.sellfy.com", "Payhip": "https://payhip.com/{u}", "LemonSqueezy": "https://{u}.lemonsqueezy.com",
        "Canva": "https://www.canva.com/@{u}", "WeHeartIt": "https://weheartit.com/{u}",
        "Fancy": "https://fancy.com/{u}", "PolyPore": "https://poly.pizza/u/{u}", "Sketchfab": "https://sketchfab.com/{u}",
        "MyMiniFactory": "https://www.myminifactory.com/users/{u}", "Imgur": "https://imgur.com/user/{u}", "Giphy": "https://giphy.com/{u}",
        "Tenor": "https://tenor.com/users/{u}", "Gfycat": "https://gfycat.com/@{u}", "9GAG": "https://9gag.com/u/{u}",
        "PicsArt": "https://picsart.com/u/{u}", "Photobucket": "https://photobucket.com/user/{u}", "ImageShack": "https://imageshack.com/user/{u}",
        "PostImages": "https://postimages.org/user/{u}", "ImgBB": "https://ibb.co/{u}", "Fotolog": "https://fotolog.com/{u}",
        "EyeEm": "https://www.eyeem.com/u/{u}", "ViewBug": "https://www.viewbug.com/member/{u}", "GuruShots": "https://gurushots.com/{u}",
        "YouPic": "https://youpic.com/photographer/{u}", "1x": "https://1x.com/member/{u}", "Photocrowd": "https://www.photocrowd.com/photographer/{u}",
        "Ello": "https://ello.co/{u}", "CarbonMade": "https://{u}.carbonmade.com", "Coroflot": "https://www.coroflot.com/{u}",
        "TumblrDesign": "https://{u}.tumblr.com", "Portfoliobox": "https://{u}.portfoliobox.net", "Format": "https://{u}.format.com"
    },
    "Крипта и финансы": {
        "OpenSea": "https://opensea.io/{u}", "Rarible": "https://rarible.com/{u}",
        "Ebay": "https://www.ebay.com/usr/{u}", "PayPal": "https://www.paypal.me/{u}",
        "Bitcointalk": "https://bitcointalk.org/index.php?action=profile;u={u}", "Etherscan": "https://etherscan.io/address/{u}", "Coinbase": "https://www.coinbase.com/{u}",
        "Kraken": "https://www.kraken.com/u/{u}", "KuCoin": "https://www.kucoin.com/account/{u}", "Bitfinex": "https://www.bitfinex.com/{u}",
        "Bittrex": "https://global.bittrex.com/{u}", "Poloniex": "https://poloniex.com/{u}", "GateIo": "https://www.gate.io/{u}",
        "Huobi": "https://www.huobi.com/{u}", "Okex": "https://www.okex.com/{u}", "Bybit": "https://www.bybit.com/{u}",
        "FTX": "https://ftx.com/{u}", "CryptoCom": "https://crypto.com/{u}", "Gemini": "https://gemini.com/{u}",
        "Robinhood": "https://robinhood.com/{u}", "Webull": "https://webull.com/{u}", "ETrade": "https://us.etrade.com/{u}",
        "TDAmeritrade": "https://tdameritrade.com/{u}", "Fidelity": "https://fidelity.com/{u}", "Schwab": "https://schwab.com/{u}",
        "Vanguard": "https://vanguard.com/{u}", "Merrill": "https://merrill.com/{u}", "Wise": "https://wise.com/pay/me/{u}",
        "Revolut": "https://revolut.me/{u}", "Monzo": "https://monzo.me/{u}", "Venmo": "https://venmo.com/u/{u}",
        "CashApp": "https://cash.app/${u}", "Zelle": "https://zellepay.com/{u}", "Blockchain": "https://www.blockchain.com/explorer/addresses/btc/{u}",
        "Bitpay": "https://bitpay.com/{u}", "Coinpayments": "https://www.coinpayments.net/{u}", "CoinGate": "https://coingate.com/{u}",
        "Cryptocompare": "https://www.cryptocompare.com/{u}", "TradingView": "https://www.tradingview.com/u/{u}/", "Investing": "https://www.investing.com/{u}",
        "SeekingAlpha": "https://seekingalpha.com/user/{u}", "YahooFinance": "https://finance.yahoo.com/{u}", 
        "MarketWatch": "https://www.marketwatch.com/{u}", "BusinessInsider": "https://www.businessinsider.com/{u}",
        "NerdWallet": "https://www.nerdwallet.com/{u}",
        "Mint": "https://mint.intuit.com/{u}", "PersonalCapital": "https://www.personalcapital.com/{u}", "Acorns": "https://www.acorns.com/{u}",
        "Betterment": "https://www.betterment.com/{u}", "Wealthfront": "https://www.wealthfront.com/{u}", "Tinkoff": "https://www.tinkoff.ru/{u}",
        "Sber": "https://www.sberbank.ru/{u}", "AlfaBank": "https://alfabank.ru/{u}", "Ozon": "https://www.ozon.ru/user/{u}",
        "Wildberries": "https://www.wildberries.ru/{u}", "YandexMarket": "https://market.yandex.ru/{u}", "Avito": "https://www.avito.ru/user/{u}",
        "Binance_API": "https://www.binance.com/bapi/composite/v1/public/profile/{u}", "Bitstamp": "https://www.bitstamp.net/{u}",
        "CEXIO": "https://cex.io/{u}", "LocalBitcoins": "https://localbitcoins.com/accounts/profile/{u}/", "Paxful": "https://paxful.com/user/{u}"
    },
    "Образование": {
        "Duolingo": "https://www.duolingo.com/profile/{u}", "Coursera": "https://www.coursera.org/user/{u}", "Stepik": "https://stepik.org/users/{u}",
        "Habr": "https://habr.com/ru/users/{u}/", "Pikabu": "https://pikabu.ru/@{u}", "MyAnimeList": "https://myanimelist.net/profile/{u}",
        "AniList": "https://anilist.co/user/{u}/", "Trakt": "https://trakt.tv/users/{u}", "Udemy": "https://www.udemy.com/user/{u}",
        "Skillshare": "https://www.skillshare.com/user/{u}", "MasterClass": "https://www.masterclass.com/{u}", "KhanAcademy": "https://www.khanacademy.org/profile/{u}",
        "EdX": "https://www.edx.org/user/{u}", "FutureLearn": "https://www.futurelearn.com/profiles/{u}", "Pluralsight": "https://www.pluralsight.com/profile/{u}",
        "Treehouse": "https://teamtreehouse.com/{u}", "Codecademy": "https://www.codecademy.com/profiles/{u}", "Udacity": "https://www.udacity.com/profile/{u}",
        "Brilliant": "https://brilliant.org/profile/{u}", "Sololearn": "https://www.sololearn.com/profile/{u}", "Mimo": "https://mimo.org/{u}",
        "DataCamp": "https://www.datacamp.com/profile/{u}", "DataQuest": "https://www.dataquest.io/profile/{u}", "GoogleDigitalGarage": "https://learndigital.withgoogle.com/{u}",
        "HubSpotAcademy": "https://academy.hubspot.com/{u}", "SemrushAcademy": "https://academy.semrush.com/{u}", "Quizlet": "https://quizlet.com/{u}",
        "Brainscape": "https://www.brainscape.com/people/{u}", "Chegg": "https://www.chegg.com/{u}", "CourseHero": "https://www.coursehero.com/profile/{u}",
        "Studocu": "https://www.studocu.com/en-us/user/{u}", "Academia": "https://{u}.academia.edu", "ResearchGate": "https://www.researchgate.net/profile/{u}",
        "GoogleScholar": "https://scholar.google.com/citations?user={u}", "ORCID": "https://orcid.org/{u}", "Scopus": "https://www.scopus.com/authid/detail.uri?authorId={u}",
        "Publons": "https://publons.com/researcher/{u}", "Loop": "https://loop.frontiersin.org/people/{u}", "SemanticScholar": "https://www.semanticscholar.org/author/{u}",
        "ArXiv": "https://arxiv.org/a/{u}", "SSRN": "https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id={u}", "JSTOR": "https://www.jstor.org/profile/{u}",
        "Springer": "https://link.springer.com/profile/{u}", "Elsevier": "https://www.elsevier.com/profile/{u}", "Wiley": "https://authorservices.wiley.com/author-resources/Journal-Authors/{u}",
        "SagePub": "https://journals.sagepub.com/profile/{u}", "TaylorFrancis": "https://www.tandfonline.com/profile/{u}", "OxfordAcademic": "https://academic.oup.com/profile/{u}",
        "CambridgeCore": "https://www.cambridge.org/core/profile/{u}", "Frontiers": "https://www.frontiersin.org/people/{u}", "MDPI": "https://www.mdpi.com/user/{u}",
        "PLOS": "https://journals.plos.org/plosone/author/{u}", "PubMed": "https://pubmed.ncbi.nlm.nih.gov/?term={u}", "ResearchID": "https://www.researcherid.com/rid/{u}"
    },
    "Спорт и здоровье": {
        "Strava": "https://www.strava.com/athletes/{u}", "MyFitnessPal": "https://www.myfitnesspal.com/profile/{u}", "Garmin": "https://connect.garmin.com/modern/profile/{u}",
        "NikeRunClub": "https://www.nike.com/member/{u}", "Runkeeper": "https://runkeeper.com/user/{u}", "AllTrails": "https://www.alltrails.com/members/{u}",
        "Peloton": "https://members.onepeloton.com/members/{u}", "Zwift": "https://www.zwift.com/athlete/{u}", "Fitbit": "https://www.fitbit.com/user/{u}",
        "Withings": "https://healthmate.withings.com/{u}", "MapMyRun": "https://www.mapmyrun.com/profile/{u}", "MapMyRide": "https://www.mapmyride.com/profile/{u}",
        "MapMyFitness": "https://www.mapmyfitness.com/profile/{u}", "Endomondo": "https://www.endomondo.com/profile/{u}", "Runtastic": "https://www.runtastic.com/{u}",
        "Bodybuilding": "https://bodyspace.bodybuilding.com/{u}", "MuscleAndFitness": "https://www.muscleandfitness.com/{u}", "MenHealth": "https://www.menshealth.com/{u}",
        "WomensHealth": "https://www.womenshealthmag.com/{u}", "Healthline": "https://www.healthline.com/{u}", "WebMD": "https://www.webmd.com/{u}",
        "MayoClinic": "https://www.mayoclinic.org/{u}", "ClevelandClinic": "https://my.clevelandclinic.org/{u}", "HopkinsMedicine": "https://www.hopkinsmedicine.org/{u}",
        "NHS": "https://www.nhs.uk/{u}", "WHO": "https://www.who.int/{u}", "CDC": "https://www.cdc.gov/{u}",
        "MedlinePlus": "https://medlineplus.gov/{u}", "DrugsCom": "https://www.drugs.com/{u}", "GoodRx": "https://www.goodrx.com/{u}",
        "Zocdoc": "https://www.zocdoc.com/{u}", "Healthgrades": "https://www.healthgrades.com/{u}", "Vitals": "https://www.vitals.com/{u}",
        "RateMDs": "https://www.ratemds.com/{u}", "Practo": "https://www.practo.com/{u}", "Docplanner": "https://www.docplanner.com/{u}",
        "Doximity": "https://www.doximity.com/{u}", "Sermo": "https://www.sermo.com/{u}", "Medscape": "https://www.medscape.com/{u}",
        "Figure1": "https://www.figure1.com/{u}", "HealthTap": "https://www.healthtap.com/{u}", "PatientsLikeMe": "https://www.patientslikeme.com/{u}",
        "MyChart": "https://mychart.com/{u}", "Epic": "https://epic.com/{u}", "Cerner": "https://cerner.com/{u}",
        "Runkeeper2": "https://runkeeper.com/{u}", "Polar": "https://flow.polar.com/{u}", "Suunto": "https://www.suunto.com/{u}",
        "Oura": "https://ouraring.com/{u}", "Whoop": "https://www.whoop.com/{u}", "AppleFitness": "https://fitness.apple.com/{u}"
    },
    "Работа и фриланс": {
        "Fiverr": "https://www.fiverr.com/{u}", "Upwork": "https://www.upwork.com/freelancers/~{u}", "Freelancer": "https://www.freelancer.com/u/{u}",
        "Toptal": "https://www.toptal.com/resume/{u}", "PeoplePerHour": "https://www.peopleperhour.com/freelancer/{u}", "Guru": "https://www.guru.com/freelancers/{u}",
        "Workana": "https://www.workana.com/freelancer/{u}", "Twine": "https://www.twine.net/{u}", "Contra": "https://contra.com/{u}",
        "Braintrust": "https://www.usebraintrust.com/{u}", "Himalayas": "https://himalayas.app/{u}", "RemoteOK": "https://remoteok.com/@{u}",
        "WeWorkRemotely": "https://weworkremotely.com/{u}", "FlexJobs": "https://flexjobs.com/{u}", "DribbbleJobs": "https://dribbble.com/{u}/jobs",
        "BehanceJobs": "https://www.behance.net/{u}/jobs", "LinkedInJobs": "https://www.linkedin.com/in/{u}/jobs", "Glassdoor": "https://www.glassdoor.com/{u}",
        "Indeed": "https://www.indeed.com/{u}", "Monster": "https://www.monster.com/{u}", "CareerBuilder": "https://www.careerbuilder.com/{u}",
        "SimplyHired": "https://www.simplyhired.com/{u}", "ZipRecruiter": "https://www.ziprecruiter.com/{u}", "Dice": "https://www.dice.com/{u}",
        "AngelList": "https://angel.co/u/{u}", "Wellfound": "https://wellfound.com/u/{u}", "YCombinator": "https://www.ycombinator.com/{u}",
        "Patreon": "https://www.patreon.com/{u}", "BuyMeACoffee": "https://www.buymeacoffee.com/{u}", "KoFi": "https://ko-fi.com/{u}",
        "Etsy": "https://www.etsy.com/shop/{u}", "Poshmark": "https://poshmark.com/closet/{u}", "Depop": "https://www.depop.com/{u}",
        "Vinted": "https://www.vinted.com/member/{u}", "Mercari": "https://www.mercari.com/u/{u}", "OfferUp": "https://offerup.com/p/{u}",
        "Letgo": "https://www.letgo.com/user/{u}", "Craigslist": "https://craigslist.org/{u}", "Gumtree": "https://www.gumtree.com/{u}",
        "OLX": "https://www.olx.com/{u}", "Youla": "https://youla.ru/user/{u}", "HeadHunter": "https://hh.ru/resume/{u}",
        "SuperJob": "https://www.superjob.ru/resume/{u}", "Rabota": "https://www.rabota.ru/{u}", "Zarplata": "https://www.zarplata.ru/{u}"
    },
    "Разное и полезное": {
        "Airbnb": "https://www.airbnb.com/users/show/{u}", "TripAdvisor": "https://www.tripadvisor.com/members/{u}", "AliExpress": "https://aliexpress.ru/store/{u}",
        "Alibaba": "https://alibaba.com/{u}", "JD": "https://jd.com/{u}", "Meituan": "https://meituan.com/{u}",
        "Kinopoisk": "https://www.kinopoisk.ru/user/{u}/", "Ivi": "https://www.ivi.ru/profile/{u}", "Okko": "https://okko.tv/user/{u}",
        "Kion": "https://kion.ru/user/{u}", "Wink": "https://wink.ru/user/{u}", "Megogo": "https://megogo.net/ru/user/{u}",
        "TwitchTV": "https://www.twitch.tv/{u}", "Uber": "https://www.uber.com/{u}", "Lyft": "https://www.lyft.com/{u}",
        "Bolt": "https://bolt.eu/{u}", "Grab": "https://www.grab.com/{u}", "Ola": "https://www.olacabs.com/{u}"
    }
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

TIMEOUT = aiohttp.ClientTimeout(total=12)
RETRIES = 1
SEMAPHORE = asyncio.Semaphore(20)

FALSE_POSITIVE_TEXTS = [
    "page not found", "user not found", "couldn't find", "not found", 
    "не найдено", "пользователь не найден", "аккаунт не найден",
    "您查看的页面找不到了", "页面不存在", "找不到页面", "该用户不存在"
]

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"\n{CYAN}=================================================={RESET}")
    print(f"{CYAN}       KAIROS // OSINT Recon Tool [BETA]{RESET}")
    print(f"{CYAN}=================================================={RESET}\n")

def extract_meta(html):
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""
    
    avatar_match = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
    if not avatar_match:
        avatar_match = re.search(r'<meta[^>]*name=["\']twitter:image["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
    avatar = avatar_match.group(1).strip() if avatar_match else ""
    
    title = re.sub(r'\s+', ' ', title)
    
    if avatar and not avatar.startswith("http"):
        avatar = ""
        
    return title, avatar

async def check_site(session, category, name, url):
    async with SEMAPHORE:
        try:
            async with session.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, ssl=False) as resp:
                if resp.status == 200:
                    text = await resp.text(encoding='utf-8', errors='ignore')
                    if any(err in text.lower() for err in FALSE_POSITIVE_TEXTS):
                        return (category, name, url, "not_found", "", "")
                    title, avatar = extract_meta(text)
                    return (category, name, url, "found", title, avatar)
                elif resp.status == 404:
                    return (category, name, url, "not_found", "", "")
                else:
                    return (category, name, url, "protected", "", "")
        except Exception:
            return (category, name, url, "protected", "", "")

def generate_html_report(username, found_sites, not_found, protected, duration, total_sites):
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kairos Report: {username}</title>
    <style>
        body {{ background-color: #0f1115; color: #ffffff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 1px solid #2a2f3a; padding-bottom: 20px; }}
        .header h1 {{ color: #22D3EE; margin: 0 0 10px 0; font-family: monospace; letter-spacing: 2px; }}
        .header p {{ margin: 5px 0; color: #8b92a5; }}
        .stats {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }}
        .stat-box {{ background: #1a1d24; padding: 15px 25px; border-radius: 10px; border: 1px solid #2a2f3a; text-align: center; min-width: 120px; }}
        .stat-box span {{ display: block; font-size: 24px; font-weight: bold; color: #22D3EE; font-family: monospace; }}
        .stat-box p {{ margin: 5px 0 0 0; color: #8b92a5; font-size: 14px; }}
        .category-title {{ color: #22D3EE; margin-top: 40px; border-bottom: 1px dashed #2a2f3a; padding-bottom: 10px; font-family: monospace; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; margin-top: 15px; }}
        .card {{ background: #1a1d24; border: 1px solid #2a2f3a; border-radius: 12px; padding: 15px; display: flex; align-items: center; gap: 15px; text-decoration: none; color: #fff; transition: 0.2s; }}
        .card:hover {{ border-color: #22D3EE; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(34,211,238,0.15); }}
        .avatar {{ width: 50px; height: 50px; border-radius: 50%; background: #2a2f3a; object-fit: cover; border: 2px solid #2a2f3a; }}
        .card:hover .avatar {{ border-color: #22D3EE; }}
        .info {{ flex: 1; overflow: hidden; }}
        .info h3 {{ margin: 0 0 5px 0; font-size: 16px; color: #22D3EE; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .info p {{ margin: 0; font-size: 12px; color: #8b92a5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .footer {{ text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #2a2f3a; color: #5c5c66; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>KAIROS // BETA</h1>
        <p>Отчет сгенерирован: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></p>
        <p>Цель: <strong style="color:#fff">{username}</strong></p>
    </div>

    <div class="stats">
        <div class="stat-box"><span>{total_sites}</span><p>Всего проверено</p></div>
        <div class="stat-box"><span>{len(found_sites)}</span><p>Найдено аккаунтов</p></div>
        <div class="stat-box"><span>{duration:.1f} сек</span><p>Время сканирования</p></div>
    </div>
"""

    categories = {}
    for site in found_sites:
        cat = site['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(site)

    for cat, sites in categories.items():
        html += f'<h2 class="category-title">[ {cat} ] - {len(sites)} шт.</h2>'
        html += '<div class="grid">'
        for site in sites:
            avatar_url = site.get('avatar', '')
            if not avatar_url:
                avatar_url = f"https://ui-avatars.com/api/?name={site['site'][0]}&background=1a1d24&color=22D3EE"
            
            bio = site.get('title', '')[:50] + "..." if site.get('title') else "Нет данных"
            
            html += f'''
            <a href="{site['url']}" target="_blank" class="card">
                <img src="{avatar_url}" class="avatar" alt="avatar" onerror="this.src='https://ui-avatars.com/api/?name={site['site'][0]}&background=1a1d24&color=22D3EE'">
                <div class="info">
                    <h3>{site['site']}</h3>
                    <p>{bio}</p>
                </div>
            </a>
            '''
        html += '</div>'

    html += '''
    <div class="footer">
        Powered by <strong>Kairos OSINT Engine</strong>
    </div>
</body>
</html>
'''
    filename = f"kairos_report_{username}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    return filename

async def main(username):
    total_sites = sum(len(sites) for sites in SITES.values())
    
    start_time = datetime.now()
    print(f"{CYAN}[i]{RESET} Цель: {YELLOW}{username}{RESET}")
    print(f"{CYAN}[i]{RESET} Всего площадок в базе: {YELLOW}{total_sites}{RESET}")
    print(f"{CYAN}[i]{RESET} Начинаем сканирование...\n")

    found_sites = []
    not_found_sites = []
    protected_sites = []
    category_counts = {cat: 0 for cat in SITES.keys()}

    connector = aiohttp.TCPConnector(limit=0, force_close=True, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for category, sites in SITES.items():
            for name, url_pattern in sites.items():
                url = url_pattern.format(u=username)
                tasks.append(check_site(session, category, name, url))
        
        for future in asyncio.as_completed(tasks):
            category, name, url, status, title, avatar = await future

            if status == "found":
                if name.endswith("_API"):
                    name = name.replace("_API", "")
                
                print(f"{GREEN}[+] {name.ljust(20)} -> {url}{RESET}")
                if title:
                    clean_title = title.replace("GitHub", "").replace("Profile", "").replace("-", "").strip()
                    if clean_title:
                        print(f"    {BLUE}Bio: {clean_title[:60]}...{RESET}")
                
                real_url = url
                if name == "GitHub":
                    real_url = f"https://github.com/{username}"
                elif name == "Reddit":
                    real_url = f"https://reddit.com/user/{username}"
                elif name == "GitLab":
                    real_url = f"https://gitlab.com/{username}"

                found_sites.append({"category": category, "site": name, "url": real_url, "title": title, "avatar": avatar})
                category_counts[category] += 1
            elif status == "not_found":
                not_found_sites.append({"category": category, "site": name, "url": url})
            else:
                protected_sites.append({"category": category, "site": name, "url": url})

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n{CYAN}=================================================={RESET}")
    print(f"{CYAN}=== СКАНИРОВАНИЕ ЗАВЕРШЕНО ==={RESET}")
    print(f"{CYAN}Всего проверено площадок: {YELLOW}{total_sites}{RESET}")
    print(f"{CYAN}Затраченное время: {YELLOW}{duration:.2f} сек.{RESET}")
    print(f"{GREEN}Найдено аккаунтов: {len(found_sites)}{RESET}")
    print(f"{RED}Свободно ников: {len(not_found_sites)}{RESET}")
    print(f"{YELLOW}Заблокировано защитой: {len(protected_sites)}{RESET}")
    
    print(f"\n{CYAN}--- СТАТИСТИКА ПО КАТЕГОРИЯМ ---{RESET}")
    for cat, count in category_counts.items():
        if count > 0:
            print(f"{GREEN}  {cat.ljust(25)}: {count} аккаунтов{RESET}")
            
    print(f"{CYAN}=================================================={RESET}\n")

    json_filename = f"kairos_{username}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump({
            "target_nickname": username,
            "date": str(end_time),
            "duration_sec": round(duration, 2),
            "total_checked": total_sites,
            "found": found_sites,
            "not_found": not_found_sites,
            "protected": protected_sites
        }, f, indent=4, ensure_ascii=False)
        
    print(f"{CYAN}[i]{RESET} JSON сохранен в файл: {json_filename}")
    
    html_filename = generate_html_report(username, found_sites, not_found_sites, protected_sites, duration, total_sites)
    print(f"{GREEN}[+] HTML-ОТЧЕТ СОЗДАН: {html_filename}{RESET}")
    print(f"{CYAN}[i]{RESET} Открой этот файл в браузере, чтобы увидеть красивый отчет!")

if __name__ == "__main__":
    print_banner()
    
    while True:
        target_input = input(f"{YELLOW}Введите никнейм для сканирования (или 'exit' для выхода): {RESET}").strip()
        
        if target_input.lower() == 'exit':
            print(f"{CYAN}[i] Выход из программы. До связи!{RESET}")
            break
            
        if not target_input:
            print(f"{RED}[!] Никнейм не может быть пустым. Попробуйте еще раз.{RESET}")
            continue
            
        asyncio.run(main(target_input))
        
        print(f"\n{CYAN}=================================================={RESET}")
        input(f"{YELLOW}Нажмите Enter, чтобы проверить другой ник...{RESET}")
        print_banner()
