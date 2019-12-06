from textblob import TextBlob
import praw
import datetime
import sys

dt = datetime.datetime.today()

reddit = praw.Reddit(client_id='EFwvR10eCo5HRw', client_secret='jkmbxFCINJVm_092NmcUDsrFCiM', password='', user_agent='USERAGENT', username='')

def get_avg_post_sentiment_dfs(parent_comment, net_sentiment, total_comments):
    #print(net_sentiment,total_comments)
    if len(parent_comment.replies) < 1:
        return [net_sentiment, total_comments]
    for comment in parent_comment.replies:
        if hasattr(comment.author, "name") and hasattr(parent_comment.author, "name"):
            tb = TextBlob(comment.body)
            sent = tb.sentiment.polarity
            net_sentiment+=sent
            total_comments+=1
            res = get_avg_post_sentiment_dfs(comment, net_sentiment, total_comments)
            net_sentiment = res[0]
            total_comments = res[1]
    return [net_sentiment, total_comments]

def get_avg_sentiment(post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None) #gets rid of "show more comments" links
    net = 0
    count = 0
    for top_level_comment in submission.comments:
        resp = get_avg_post_sentiment_dfs(top_level_comment, 0, 0)
        net += resp[0]
        count += resp[1]
    if count > 0:
        return net/count
    else:
        return 0

def get_subreddit_post_sentiments(sub):
    post_dict = dict()
    i = 1
    lim = 100
    
    f = open("subreddit_collected_data_raw.csv", 'a')
    for submission in reddit.subreddit(sub).top('week', limit=lim):
        sys.stdout.write("\rPost"+str(i)+"/100       ")
        sys.stdout.flush()
        res = get_avg_sentiment(submission.id)
        if submission.subreddit.display_name not in post_dict:
            post_dict[sub] = {"net_sentiment": res, "post_count":1}
        else:
            post_dict[sub]["net_sentiment"]+=res
            post_dict[sub]["post_count"]+=1 #second+ time we saw this subreddit
        i+=1
        if submission.over_18:
            f.write(submission.id+","+str(res)+","+sub+",FALSE\n")
        else:
            f.write(submission.id+","+str(res)+","+sub+",TRUE\n")
    sys.stdout.write("\n")
    f.close()
    return post_dict

def dict_to_csv(d, collection_id):
    f = open("subreddit_collected_data.csv", 'a')
    for sub in d.keys():
        f.write(str(collection_id)+","+sub+","+str(d[sub]["net_sentiment"])+","+str(d[sub]["post_count"])+"\n")
    f.close()
    return

def get_subreddits():
    f = open("combined_data.csv")
    l = []
    next(f)
    lines = f.readlines()
    for line in lines:
        contents = line.split(",")
        l.append(contents[0])
    print(l)
    return l


d = dict()
start_idx=369
subreddit_list_full = ['gaming', 'funny', 'memes', 'dankmemes', 'wholesomememes', 'aww', 'PublicFreakout', 'blursedimages', 'pics', 'nextfuckinglevel', 'mildlyinteresting', 'rareinsults', 'suspiciouslyspecific', 'BlackPeopleTwitter', 'HistoryMemes', 'PewdiepieSubmissions', 'instantkarma', 'trippinthroughtime', 'Unexpected', 'comedyheaven', 'teenagers', 'todayilearned', 'WhitePeopleTwitter', 'ProgrammerHumor', 'Showerthoughts', 'lifehacks', 'AskReddit', 'interestingasfuck', 'WatchPeopleDieInside', 'cursedcomments', 'Damnthatsinteresting', 'science', 'BikiniBottomTwitter', 'me_irl', 'NatureIsFuckingLit', 'Wellthatsucks', 'blackmagicfuckery', 'MadeMeSmile', 'sadcringe', 'imsorryjon', 'HongKong', 'BrandNewSentence', 'therewasanattempt', '2meirl4meirl', 'suicidebywords', 'TIHI', 'Eyebleach', 'gifs', 'trashy', 'StarWars', 'space', 'PrequelMemes', 'Futurology', 'starterpacks', 'politics', 'iamatotalpieceofshit', 'blessedimages', 'Minecraft', 'madlads', 'insanepeoplefacebook', 'oddlysatisfying', 'agedlikemilk', 'GetMotivated', 'HumansBeingBros', 'instant_regret', 'OldSchoolCool', 'modernwarfare', 'worldnews', 'facepalm', 'comics', 'leagueoflegends', 'news', 'Whatcouldgowrong', 'DunderMifflin', 'HighQualityGifs', 'oddlyterrifying', 'HolUp', 'dndmemes', 'EarthPorn', 'insaneparents', 'Tinder', 'tifu', 'technicallythetruth', 'WTF', 'ThatsInsane', 'pcmasterrace', 'toptalent', 'rarepuppers', 'AnimalsBeingDerps', 'natureismetal', 'photoshopbattles', 'quityourbullshit', 'holdmyfeedingtube', 'mildlyinfuriating', 'Bossfight', 'KidsAreFuckingStupid', 'unpopularopinion', 'MakeMeSuffer', 'nevertellmetheodds', 'woof_irl', 'IdiotsInCars', 'freefolk', 'youngpeopleyoutube', 'technology', 'ShitPostCrusaders', 'wholesomegifs', 'meirl', 'dataisbeautiful', 'BetterEveryLoop', 'PeopleFuckingDying', 'MemeEconomy', 'tumblr', 'cursedimages', 'AbsoluteUnits', 'wholesomeanimemes', 'LateStageCapitalism', 'atheism', 'coolguides', 'MovieDetails', 'fightporn', 'rickandmorty', 'KeanuBeingAwesome', 'comedyhomicide', 'confusing_perspective', 'perfectlycutscreams', 'gonewild', 'videos', 'FellowKids', 'shittymoviedetails', 'forbiddensnacks', 'fakehistoryporn', 'ShittyLifeProTips', 'AteTheOnion', 'HydroHomies', 'hmmm', 'dank_meme', 'maybemaybemaybe', 'Cringetopia', 'thanosdidnothingwrong', 'CozyPlaces', 'dontputyourdickinthat', 'FuckYouKaren', 'specializedtools', 'lotrmemes', 'Art', 'AbruptChaos', 'food', 'Jokes', 'bonehurtingjuice', 'IAmA', 'inthesoulstone', 'formula1', 'DiWHY', 'AnimalsBeingBros', 'niceguys', 'Rainbow6', 'PoliticalHumor', 'wholesomebpt', 'TikTokCringe', 'greentext', 'antimeme', 'AmItheAsshole', '2healthbars', 'assholedesign', 'gatekeeping', 'WitchesVsPatriarchy', 'absolutelynotmeirl', 'ANormalDayInRussia', 'thisismylifenow', 'PornhubComments', 'NoStupidQuestions', 'marvelmemes', 'CrappyDesign', 'nottheonion', 'yesyesyesyesno', 'books', 'DeepFriedMemes', 'boomershumor', 'JusticeServed', 'reddeadredemption', 'ChildrenFallingOver', 'SuddenlyGay', 'soccer', 'WeWantPlates', 'NintendoSwitch', 'apexlegends', 'ATBGE', 'justneckbeardthings', 'TwoXChromosomes', 'CasualUK', 'awfuleverything', 'Awwducational', 'likeus', 'intermittentfasting', 'disneyvacation', 'nsfw', 'LivestreamFail', 'copypasta', 'gifsthatkeepongiving', 'television', 'DnD', 'u_SrGrafo', 'absolutelynotme_irl', 'anime_irl', 'australia', 'europe', 'BoneAppleTea', 'notliketheothergirls', 'marvelstudios', 'TheLastAirbender', 'raimimemes', 'Overwatch', 'ImGoingToHellForThis', 'godtiersuperpowers', 'whitepeoplegifs', 'teefies', 'WinStupidPrizes', 'boottoobig', 'nba', 'FortNiteBR', 'AskOuija', 'wow', 'nonononoyes', 'UrbanHell', 'pokemon', 'TopMindsOfReddit', 'FoodPorn', 'rimjob_steve', 'AskMen', 'PandR', 'BeAmazed', 'menwritingwomen', 'softwaregore', 'cringepics', 'lego', 'vaxxhappened', 'badwomensanatomy', 'antiMLM', 'thatHappened', 'skyrim', 'oldpeoplefacebook', 'CatastrophicFailure', 'nukedmemes', 'InsanePeopleQuora', 'PenmanshipPorn', 'DidntKnowIWantedThat', 'HumansAreMetal', 'WhatsWrongWithYourDog', 'WritingPrompts', 'crappyoffbrands', 'Chonkers', 'ItemShop', 'meme', 'ScottishPeopleTwitter', 'Instagramreality', 'trees', 'woahdude', 'FunnyandSad', 'explainlikeimfive', 'tippytaps', 'GamersRiseUp', 'pussypassdenied', 'DnDGreentext', 'shittyrainbow6', 'SandersForPresident', 'HadToHurt', 'SmashBrosUltimate', 'Catswithjobs', 'SweatyPalms', 'RealGirls', 'ChoosingBeggars', 'NoahGetTheBoat', 'AAAAAAAAAAAAAAAAA', 'worldpolitics', 'holdmyredbull', '2007scape', 'terriblefacebookmemes', 'ToiletPaperUSA', 'FUCKYOUINPARTICULAR', 'gatesopencomeonin', 'Memes_Of_The_Dank', 'shittysuperpowers', 'pyrocynical', 'Botchedsurgeries', 'MaliciousCompliance', 'pawg', 'dadjokes', 'MEOW_IRL', 'sweden', 'destiny2', 'bodyperfection', 'shittyrobots', 'SequelMemes', 'dogswithjobs', 'sports', '4chan', 'zelda', 'PetiteGoneWild', 'TheMonkeysPaw', 'AsiansGoneWild', 'oddlyspecific', 'StarWarsBattlefront', 'Terraria', 'SelfAwarewolves', 'BiggerThanYouThought', 'StrangerThings', 'Gamingcirclejerk', 'toastme', 'DestinyTheGame', 'whatisthisthing', 'ExpectationVsReality', 'RocketLeague', '4PanelCringe', 'BirdsArentReal', 'lgbt', 'SapphoAndHerFriend', 'DadReflexes', 'reactiongifs', 'ComedyNecrophilia', 'animalsdoingstuff', 'INEEEEDIT', 'Cursed_Images', 'adorableporn', 'StardewValley', 'beetlejuicing', 'gtaonline', 'smoobypost', 'bigtiddygothgf', 'iamverybadass', 'MemeTemplatesOfficial', '13or30', 'TwoSentenceHorror', 'Documentaries', 'ConvenientCop', 'halo', 'standupshots', 'southpark', 'surrealmemes', 'drawing', 'LeopardsAteMyFace', 'DankMemesFromSite19', 'OutOfTheLoop', 'formuladank', 'cumsluts', 'wholesomejojo', 'MurderedByWords', 'LifeProTips', 'CFB', 'comedynecromancy', 'clevercomebacks', 'relationship_advice', 'EmpireDidNothingWrong', 'ihadastroke', 'GifRecipes', 'EntitledBitch', 'educationalgifs', 'dontyouknowwhoiam', 'Neverbrokeabone', 'UpliftingNews', 'GlobalOffensive', 'Breath_of_the_Wild', 'ComedyCemetery', 'PokemonSwordAndShield', 'evilbuildings', 'AdviceAnimals', 'hearthstone', 'im14andthisisdeep', 'iamverysmart', 'holdmycosmo', 'movies', 'MostBeautiful', 'conspiracy', 'TheRightCantMeme', 'GamePhysics', 'nonutnovember', 'teslamotors', 'brooklynninenine', 'PraiseTheCameraMan', 'NSFW_GIF', 'hmmmgifs', 'BokuNoHeroAcademia', 'lostredditors', 'RoastMe', 'bi_irl', 'tooktoomuch', 'Zoomies', 'ass', 'DesignPorn', 'tf2', 'LegalTeens', 'BeforeNAfterAdoption', 'holdmycatnip', 'medizzy', 'wallstreetbets', 'theydidthemath', 'blunderyears', 'OTMemes', 'MapPorn', 'TheMandalorianTV', 'battlestations', '2meirl42meirl4meirl', 'OopsDidntMeanTo', 'IncelTears', 'Frugal', 'csgo', 'collegesluts', 'FiftyFifty', 'BustyPetite', 'FragileWhiteRedditor', 'JustBootThings', 'ENLIGHTENEDCENTRISM', 'SCP', 'donthelpjustfilm', 'holdmyfries', 'trebuchetmemes', 'MonsterHunterWorld', 'ksi', 'bisexual', 'PetTheDamnDog', 'confession', 'wholesomegreentext', 'ArtefactPorn', 'LeagueOfMemes', 'ContagiousLaughter', 'bigboye', 'AnimalsBeingJerks', 'OurPresident', 'youseeingthisshit', 'Bad_Cop_No_Donut', 'canada', 'Perfectfit', 'woodworking', 'reallifedoodles', 'ThatLookedExpensive', 'xboxone', 'mallninjashit', 'NobodyAsked', 'UNBGBBIIVCHIDCTIICBG', 'YouShouldKnow', 'mechanical_gifs', 'AccidentalRacism', 'LipsThatGrip', 'gadgets', 'Kanye', 'Catswhoyell', 'ihavesex', 'perfectloops', 'yesyesyesno', 'DemocraticSocialism', 'Steam', 'IASIP', 'Instantregret', 'badUIbattles', 'watchpeoplesurvive', 'iamveryrandom', 'askscience', 'itookapicture', 'UnethicalLifeProTips', 'PunPatrol', 'dating_advice', 'shittyfoodporn', 'AskHistorians', 'HumanForScale', 'tuckedinkitties', 'MinecraftMemes', 'TooAfraidToAsk', 'PS4', 'bertstrips', 'discordapp']
subreddit_list = subreddit_list_full[start_idx:]
print("Starting code run starting at /r/"+subreddit_list[0])
i = 1+start_idx
for sr in subreddit_list:
    print(str(i)+"/"+str(len(subreddit_list_full)))
    print("/r/"+sr)
    d = get_subreddit_post_sentiments(sr)
    print("Done\nWriting to file...")
    dict_to_csv(d, dt.day)
    print("Done\n")
    i+=1
print("Done everything\n")
