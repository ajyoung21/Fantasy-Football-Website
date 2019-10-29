import requests
import pandas as pd
import datetime
import webbrowser



#Figures out what week it currently is.
if datetime.datetime.now()<datetime.datetime(2019,9,11):
    week = 1
elif datetime.datetime.now()<datetime.datetime(2019,9,18):
        week = 2
elif datetime.datetime.now()<datetime.datetime(2019,9,25):
        week = 3
elif datetime.datetime.now()<datetime.datetime(2019,10,2):
        week = 4
elif datetime.datetime.now()<datetime.datetime(2019,10,9):
        week = 5
elif datetime.datetime.now()<datetime.datetime(2019,10,16):
        week = 6
elif datetime.datetime.now()<datetime.datetime(2019,10,23):
        week = 7
elif datetime.datetime.now()<datetime.datetime(2019,10,30):
        week = 8


#Hack into league
league_id = 40107500
season = 2019
swid = '{9F3AC23C-F543-45B2-BAC2-3CF543D5B29D}'
espn_s2 = "AECSpbbNBlsL7hzRBkq2LIPalKGU5xHDGKj08DyTXCcxzcSc5ybZGT0IkEWRk9YAwJms3aEBYjW0tEUqSdQmXkhDLQ%2FsKijWwLg%2FCNaab%2BfZ4onYOVoP4gZbsONETxdovhe9FKIdiznUV60IsvLfqCnEvhP3s4hsvn6V%2BdFpCyklQTuP5OiZ1phnrYstX9Yjm%2FqpfeU7lCjnAirszSV9IJfYZQfy8bDu8CNt2e3sjkIjtwG%2FMTx3qWtQZqbQ4g7owm6t%2B6NjkFpYoDGBGO7nzSg8"



url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + \
      str(season) + '/segments/0/leagues/' + str(league_id) + \
      '?view=mMatchup&view=mMatchupScore'

r = requests.get(url,
                 params={'scoringPeriodId': week},
                 cookies={"SWID": swid, "espn_s2": espn_s2})

d = r.json()    

#Use Pandas to scrape from site
df = [[
        game['matchupPeriodId'],
        game['home']['teamId'], game['home']['totalPoints'],
        game['away']['teamId'], game['away']['totalPoints']
    ] for game in d['schedule']]
df = pd.DataFrame(df, columns=['Week', 'Team1', 'Score1', 'Team2', 'Score2'])
df['Type'] = ['Regular' if w<=14 else 'Playoff' for w in df['Week']]
df.head()

#Convert to list bc Idk how to use pandas dataframes
matchup_list = df.values.tolist()


#Change TeamIDs to Team Names
team_names = ['Commissioner Gordon', 'The T-Boners', 'Raleigh Primeshoppers', 'Produce Warriors', 'Team Huston', 'The Phantom Chef', 'WHOLE DOODS FC', 'Team Pegasus', 'Wack Wack', 'The Butcher']
team_num = [1,2,3,4,5,6,7,8,9,10]

#Define Logos and GIFs for each team




Colby_GIF = '<img src="Colby.gif" alt="ColbyGIF" style="width:168px;height:120px;">'
Avi_GIF = '<img src="Avi.gif" alt="AviGIF" style="width:168px;height:120px;">'
Aaron_GIF = '<img src="Aaron.gif" alt="AaronGIF" style="width:168px;height:120px;">'
Alex_GIF = '<img src="Whole_Doods.gif" alt="AlexGIF" style="width:168px;height:120px;">'
Allison_Gif = '<img src="Allison.gif" alt="AllisonGIF" style="width:168px;height:120px;">'
Tommy_GIF = '<img src="Tommy.gif" alt="TommyGIF" style="width:168px;height:120px;">'

team_GIFs = [ Colby_GIF,'' , Avi_GIF, '', Aaron_GIF, '', Alex_GIF, Allison_Gif,'', Tommy_GIF]



flipped_GIF = """<style> img:hover {-webkit-transform: scaleX(-1); transform: scaleX(-1);} </style>"""





#It wouldn't get Tommy's name for whatever reason...
for m in range(0, len(matchup_list)):
    for i in range(0,10):
        if matchup_list[m][1] == team_num[i]:
            matchup_list[m][1] = f"{flipped_GIF}{team_GIFs[i]}{team_names[i]}"
        if matchup_list[m][3] == team_num[i]:
            matchup_list[m][3] = f"{team_names[i]}{team_GIFs[i]}"

results = []
for ml in range(0,len(matchup_list)):
    team_one = str(matchup_list[ml][1])  
    score_one = str(matchup_list[ml][2])
    team_two = str(matchup_list[ml][3])
    score_two = str(matchup_list[ml][4]) 
    if score_one > score_two:
        results.append([team_one,'W'])
        results.append([team_two, 'L'])
    if score_one < score_two:
        results.append([team_one,'L'])
        results.append([team_two, 'W'])
    else:
        results.append([team_one,'T'])
        results.append([team_two, 'T'])
records = {}         
for team in team_names:
    win_counter = 0
    loss_counter = 0
    for result in results:
        if result[1] == 'W':
            win_counter = win_counter + 1
        if result[1] == 'L':
            loss_counter = loss_counter + 1
        records.update( {f'{team}': [win_counter,loss_counter]})
 
East_Cary_names = ['Commissioner Gordon', 'Raleigh Primeshoppers', 'Team Huston', 'WHOLE DOODS FC', 'Wack Wack']
West_Cary_names = ['The T-Boners', 'Produce Warriors', 'The Phantom Chef', 'Team Pegasus', 'The Butcher']
team_num = [1,2,3,4,5,6,7,8,9,10]



team_names2 = []
for name in team_names:
    team_names2.append(f'{name} ({records[name][0]}-{records[name][1]})')


Colby_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[0]}</div><img src="Colby.png"/></a>'
Andy_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[1]}</div><img src="Andy.png"/></a>'
Avi_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[2]}</div><img src="AviLogo.png"/></a>'
Chris_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[3]}</div><img src="Chris_Logo.png"/></a>'
Aaron_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[4]}</div><img src="Aaron.png"/></a>'
Tim_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[5]}</div><img src="Tim_Logo.png"/></a>'
Alex_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[6]}</div><img src="WholeDoods2.jpg"/></a>'
Allison_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[7]}</div><img src="Allison.png"/></a>'
Daniel_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[8]}</div><img src="Daniel_Logo.png"/></a>'
Tommy_Logo = f'<a class="img" href="#"><div class="img__overlay">{team_names2[9]}</div><img src="TommyLogo.png"/></a>'



East_Cary_Standings =  f"""<div id="banner">
    <div class="inline-block">
        {Colby_Logo}
    </div>
    <div class="inline-block">
        {Avi_Logo}
    </div>  
    <div class="inline-block">
        {Aaron_Logo}
    </div>
    <div class="inline-block">
        {Alex_Logo}
    </div>
    <div class="inline-block">
        {Daniel_Logo}
    </div>
</div>"""

West_Cary_Standings =  f"""<div id="banner">
    <div class="inline-block">
        {Andy_Logo}
    </div>
    <div class="inline-block">
        {Chris_Logo}
    </div>  
    <div class="inline-block">
        {Tim_Logo}
    </div>
    <div class="inline-block">
        {Allison_Logo}
    </div>
    <div class="inline-block">
        {Tommy_Logo}
    </div>
</div>"""

html_str = f"""

<!DOCTYPE html>
<html>
<h1 style='text-align: center; color:mediumseagreen'> The Whole West Cary League  </h1>
{East_Cary_Standings}
{West_Cary_Standings}

<body style="background-color:powderblue;">

"""
style = """


<style>
.inline-block {
   display: inline-block;
}
.dropbtn {
  background-color: #4CAF50;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
}

.dropdown {
  position: relative;
  justify-content; center;
  display: inline-block;
}

.dropdown-content {
  display: none;
  justify-content: center;
  position: absolute;
  background-color: #18a7ba;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}
div{
    text-align:center;
}

.dropdown-content a {
  color: white;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {background-color: #ddd;}

.dropdown:hover .dropdown-content {display: block;}

.dropdown:hover .dropbtn {background-color: #3e8e41;}
.dropdown {text-align:center;}
.button, .dropdown-menu {margin:10px auto}
.dropdown-menu {width:200px; left:50%; margin-left:-100px;}
.img {
  border-radius: 100%;
      display: flex;
      flex: 0 0 150px;
      height: 150px;
      justify-content: center;
      overflow: hidden;
      position: relative;
      width: 150px;
  }   
  .img img {
      height: 100%;
    }
    .img__overlay {
      align-items: center;
      bottom: 0;
      display: flex;
      justify-content: center;
      left: 0;
      opacity: 0;
      position: absolute;
      right: 0;
      top: 0;
      transition: opacity 0s;
      z-index: 1;
    }
    .img__overlay:hover {
    opacity: 1;
  }
  
    .img__overlay {
      background-color: rgba(46,204,113,0.4);
      background: linear-gradient(65deg, rgba(46,204,113,0.4), rgba(0,0,102,0.2));
      color: #FAFAFA;
      font-size: 18px;
    }

  
   
  </a>

</style>

"""
html_str = html_str + style
html_str = html_str + f""" 


"""



#Print the matchup based on the week. Winning = Green, Losing = Red, Tie = Blue
def Create_Scoreboard(filename, week):
    filename = 'Weeks/' + filename
    week = week
    new_html_str = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title> Week {week}: The Whole West Cary League</title>
</head>
    
    
    

<link rel="stylesheet" type="text/css" href="../style.css">

<h1 style='text-align:center;'> Scoreboard (Week {week}) </h1>
 
<h4 style='text-align:center;'> <div class="dropdown"; style='text-align:center'>
  <button class="dropbtn">Select Week</button>
  <div class="dropdown-content">
    <a href="../index.html">Home/Standings</a>
    <a href="week1.html">Week 1</a>
    <a href="week2.html">Week 2</a>
    <a href="week3.html">Week 3</a>
    <a href="week4.html">Week 4</a>
    <a href="week5.html">Week 5</a>
    <a href="week6.html">Week 6</a>
    <a href="week7.html">Week 7</a>
    <a href="week8.html">Week 8</a>
    <a href="week9.html">Week 9</a>
    <a href="week10.html">Week 10</a>
    <a href="week11.html">Week 11</a>
    <a href="week12.html">Week 12</a>
    <a href="week13.html">Week 13</a>
    <a href="week14.html">Week 14 (Playoffs)</a>
    <a href="week15.html">Week 15 (Playoffs)</a>
    </div>
  </div>
</div> </h4>

<table style='width:100%'> """



    for ml in range(0,len(matchup_list)):
        
        if int(matchup_list[ml][0]) == int(week):
            team_one = str(matchup_list[ml][1])  
            score_one = str(matchup_list[ml][2])
            team_two = str(matchup_list[ml][3])
            score_two = str(matchup_list[ml][4])
            if score_one > score_two:
                new_html_str = new_html_str + f"""
                <tr>
                <td><div class="win"> {team_one} {score_one}</div></td>
                <td> vs. </td>
                <td><div class="lose"> {score_two} {team_two}</div></td>
                </tr>"""
            if score_two > score_one:
                new_html_str = new_html_str + f"""
                <tr>
                <td><div class="lose"> {team_one} {score_one}</div></td>
                <td> vs. </td>
                <td><div class="win"> {score_two} {team_two}</div></td>
                </tr>"""

 
    new_html_str = new_html_str + """</table>
    </body>
    </html>"""
    if filename == 'hi.html':
        Html_file= open(filename,"w")
        Html_file.write(html_str + new_html_str)
        
    else:
        Html_file= open(filename,"w")
        Html_file.write(new_html_str)
        Html_file.close()

# Create_Scoreboard('index.html', week)
for i in range(1,16):
    filename = f'week{i}.html'
    week = i
    Create_Scoreboard(filename, week)




