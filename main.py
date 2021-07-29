import numpy as np
import pandas as pd
import plotly.offline as py
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

color = sns.color_palette()
py.init_notebook_mode(connected=True)
# get_ipython().run_line_magic('matplotlib', 'inline')
pio.renderers.default = 'browser'


# open the text file to see
def run_profile_report(csv):
    df = pd.read_csv(csv)
    profile = df.profile_report(title="Demographic Analysis",
                                dataset={
                                    "description": "This profiling report was generated for Explore Hacks by Sarah Dufays, Jennifer Chiou, Mudit Marwaha, and Alizain Fatehali",
                                    "copyright_holder": "Sarah Dufays",
                                    "copyright_year": "2021"
                                })
    profile.to_file(output_file="<test>.html")


# use this to find how many occurences of a value there is in a column
def sum(csv, column, value):
    df = pd.read_csv(csv)
    result = (df[column].values == value).sum()
    return result


def pi_graph(csv, column, graph_title):
    df = pd.read_csv(csv)
    dist = df[column].value_counts()
    colors = ['mediumturquoise', 'darkorange']
    trace = go.Pie(values=(np.array(dist)), labels=dist.index)
    layout = go.Layout(title=graph_title)
    fig = go.Figure(trace, layout)
    fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.show()


def box_and_whisker(csv, x_axis, y_axis, title):
    df = pd.read_csv(csv)
    fig = px.box(df, x=x_axis, y=y_axis)
    fig.update_traces(marker_color="midnightblue", marker_line_color='rgb(80,203,147)',
                      marker_line_width=1.5)
    fig.update_layout(title_text=title)
    fig.show()


def scatter_plot(csv, horizontal_axis, vertical_axis, plot_title):
    df = pd.read_csv(csv)
    fig = px.scatter(df, x=horizontal_axis, y=vertical_axis)
    fig.update_traces(marker_color="turquoise", marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5)
    fig.update_layout(title_text=plot_title)
    fig.show()


def diversity(csv):
    df = pd.read_csv(csv)
    diversity_score = 5

    # gender
    total_males = sum(csv, 'Sex', 'M')
    num_rows = df.shape[0]
    percentage_male = total_males / num_rows * 100
    total_females = sum(csv, 'Sex', 'F')
    num_rows = df.shape[0]
    percentage_female = total_females / num_rows * 100
    pi_graph(csv, "Sex", "Number of Males vs. Females")
    print("\n{:0.1f} % of your company is male and {:0.1f} % of your company is female\n".format(percentage_male,
                                                                                                 percentage_female))
    if percentage_female < 45:
        print("\nConsider hiring more female employees and addressing implicit gender biases in your company\n")
        # updates Diversity Score
        diversity_score = diversity_score - 1
    elif percentage_male < 45:
        print("Consider hiring more male employees and addressing implicit gender biases in your company")
        diversity_score = diversity_score - 1
    else:
        print("You have a great gender ratio in your company!")

    # race
    pi_graph(csv, "RaceDesc", "Race Distribution")
    num_races = df.RaceDesc.nunique()
    # creates a sorted list of the percentages of each race
    percent_white = sum(csv, "RaceDesc", "White") / num_rows * 100
    percent_black = sum(csv, "RaceDesc", "Black or African American") / num_rows * 100
    percent_hisp = sum(csv, "RaceDesc", "White/Hispanic") / num_rows * 100
    percent_asian = sum(csv, "RaceDesc", "Asian") / num_rows * 100
    percent_mixed = sum(csv, "RaceDesc", "Two or more races") / num_rows * 100
    percent_amerind = sum(csv, "RaceDesc", "American Indian or Alaska Native") / num_rows * 100
    percent_list = [percent_white, percent_black, percent_hisp, percent_asian, percent_mixed, percent_amerind]
    percent_list.sort()

    if num_races < 5:
        print(
            "Consider hiring diversely. In your business, you only have representation from %d races. Workplace diversity is key to success in your business, whether for different perspectives, unique approaches,increased creativity, or valuable insights that can increase DEI, productivity and profits within your company." % num_races)
        diversity_score = diversity_score - 1
    elif percent_white >= 50:
        print("Consider hiring diversely. Your business is %d percent white, so if the area your company is located in is more diverse than that, you should consider diversifying to give more people opportunities." % percent_white)
        diversity_score = diversity_score - 1
    elif (percent_list[1] < 5) or (percent_list[2] < 5) or (percent_list[3] < 5) or (percent_list[4] < 5):
        print("Consider hiring diversely. One or more minorities is underrepresented within your company (please view the pie chart for more detail), which can stifle creativity.")
        diversity_score = diversity_score - 1
    else:
        print(
            "\nYou have representation from %d different races in your company! Check the pi chart of your company's Race Distribution to ensure that minorities are fairly represented." % num_races)

    print("YOUR DIVERSITY SCORE: On a scale of 0-5 (5 being the most diverse), you have a score of " + str(diversity_score) + ".\n\n")


def equity(csv):
    df = pd.read_csv(csv)
    average_salary = int(df['Salary'].mean())
    print("The average salary in your company is $" + str(average_salary))
    equity_score = 6

    box_and_whisker(csv, "Sex", "Salary", "Correlation Between Employee Gender and Salary")
    grouped_df_sex = df.groupby("Sex")
    # creates data frame of averages, grouped by sex
    mean_df = grouped_df_sex.mean()
    fem_avg_salary = round(mean_df.at["F", "Salary"])
    male_avg_salary = round(mean_df.at["M", "Salary"])
    if fem_avg_salary < male_avg_salary - 2000:
        print("The average salary for females in your company is $" + str(format(fem_avg_salary)) + ", and the average salary for males in your company is $" + str(format(male_avg_salary)) + ". Your average male salary is greater than that of females, so it is important to consider if you are giving more job opportunities to males, or if you are promoting one gender more than the other. Please remember that your company's productivity will increase if you provide everyone with an equitable chance of succeeding.")
        equity_score = equity_score - 1
    else:
        print("Your company is equitable for both women and men, but still head over to our Solutions Tab to see how you can improve even more!")

    box_and_whisker(csv, "RaceDesc", "Salary", "Correlation Between Employee Race and Salary")
    # creates data frame of averages, grouped by race
    grouped_df_race = df.groupby("RaceDesc")
    race_mean_df = grouped_df_race.mean()
    white_avg_salary = round(race_mean_df.at["White", "Salary"])
    hisp_avg_salary = round(race_mean_df.at["White/Hispanic", "Salary"])
    black_avg_salary = round(race_mean_df.at["Black or African American", "Salary"])
    asian_avg_salary = round(race_mean_df.at["Asian", "Salary"])
    mixed_avg_salary = round(race_mean_df.at["Two or more races", "Salary"])
    amerind_avg_salary = round(race_mean_df.at["American Indian or Alaska Native", "Salary"])

    if (hisp_avg_salary < white_avg_salary - 2000):
        print("Consider looking into the salaries of your Hispanic employees, as the average salary for Hispanic employees is lower than that of white employees.")
        equity_score = equity_score - 1
    elif (black_avg_salary < white_avg_salary - 2000):
        print("Consider looking into the salaries of your Black/African American employees, as the average salary for those employees is lower than that of white employees.")
        equity_score = equity_score - 1
    elif (asian_avg_salary < white_avg_salary - 2000):
        print("Consider looking into the salaries of your Asian employees, as the average salary for Asian employees is lower than that of white employees.")
        equity_score = equity_score - 1
    elif (mixed_avg_salary < white_avg_salary - 2000):
        print("Consider looking into the salaries of your mixed race employees, as the average salary for those employees is lower than that of white employees.")
    elif (amerind_avg_salary < white_avg_salary - 2000):
        print("Consider looking into the salaries of your American Indian/Alaska Native employees, as the average salary for those employees is lower than that of white employees.")
        equity_score = equity_score - 1
    else:
        print("There is no significant racial inequities in your employees' salary, but we encourage you to head to the Solutions Tab for ideas on how to become even more inclusive!")

    print("YOUR EQUITY SCORE: On a scale of 0-6 (6 being the most equitable), you have a score of " + str(equity_score) + ".\n\n")


def inclusion(csv):
    df = pd.read_csv(csv)
    inclusion_score = 7
    # demographic vs. satisfaction

    box_and_whisker(csv, "RaceDesc", "EmpSatisfaction", "Correlation Between Employee Race and Satisfaction")
    grouped_df_race = df.groupby("RaceDesc")
    race_mean_df = grouped_df_race.mean()
    white_avg_satisf = round(race_mean_df.at["White", "EmpSatisfaction"])
    hisp_avg_satisf = round(race_mean_df.at["White/Hispanic", "EmpSatisfaction"])
    black_avg_satisf = round(race_mean_df.at["Black or African American", "EmpSatisfaction"])
    asian_avg_satisf = round(race_mean_df.at["Asian", "EmpSatisfaction"])
    mixed_avg_satisf = round(race_mean_df.at["Two or more races", "EmpSatisfaction"])
    amerind_avg_satisf = round(race_mean_df.at["American Indian or Alaska Native", "EmpSatisfaction"])

    if (hisp_avg_satisf < white_avg_satisf):
        print("Your Hispanic employees may be less satisfied with their work environment than your white employees. Try to think of ways to make the workplace more inclusive of them, and see our Solutions Tab for suggestions.")
        inclusion_score = inclusion_score - 1
    elif (black_avg_satisf < white_avg_satisf):
        print("Your black/African American employees may be less satisfied with their work environment than your white employees. Try to think of ways to make the workplace more inclusive of them, and see our Solutions Tab for suggestions.")
        inclusion_score = inclusion_score - 1
    elif (asian_avg_satisf < white_avg_satisf):
        print("Your Asian employees may be less satisfied with their work environment than your white employees. Try to think of ways to make the workplace more inclusive of them, and see our Solutions Tab for suggestions.")
        inclusion_score = inclusion_score - 1
    elif (mixed_avg_satisf < white_avg_satisf):
        print("Your mixed race employees may be less satisfied with their work environment than your white employees. Try to think of ways to make the workplace more inclusive of them, and see our Solutions Tab for suggestions.")
        inclusion_score = inclusion_score - 1
    elif (amerind_avg_satisf < white_avg_satisf):
        print("Your American Indian/Alaska Native employees may be less satisfied with their work environment than your white employees. Try to think of ways to make the workplace more inclusive of them, and see our Solutions Tab for suggestions.")
        inclusion_score = inclusion_score - 1
    else:
        print("Your employees are equally satisfied regardless of race, so look to the box and whisker plot we've provided to help you improve employee satisfaction as a whole.")

    box_and_whisker(csv, "Sex", "EmpSatisfaction", "Correlation Between Employee Gender and Satisfaction")
    grouped_df_sex = df.groupby("Sex")
    mean_df = grouped_df_sex.mean()
    fem_avg_satisf = round(mean_df.at["F", "EmpSatisfaction"])
    male_avg_satisf = round(mean_df.at["M", "EmpSatisfaction"])

    if fem_avg_satisf < male_avg_satisf:
        print("Your female employees seem to be less satisfied than your male employees. This can be solved by creating a more inclusive environment through open discussions and reflection. Please see our Solutions Tab for a more in-depth recommendation.")
        inclusion_score = inclusion_score - 1
    elif male_avg_satisf < fem_avg_satisf:
        print("Your male employees seem to be less satisfied than your female employees. Think about why this may be, and address it through open discussion. Please see our Solutions Tab for a more in-depth way to do so.")
        inclusion_score = inclusion_score - 1
    else:
        print("Your employees seem to be equally satisfied regardless of gender, but look at the box and whisker plot we've provided for you to see if you can improve satisfaction as a whole.")

    # engagement by gender
    scatter_plot(csv, "Sex", "EngagementSurvey", "Employee Engagement by Gender")
    fem_avg_engage = round(mean_df.at["F", "EngagementSurvey"])
    male_avg_engage = round(mean_df.at["M", "EngagementSurvey"])

    if fem_avg_engage < male_avg_engage:
        print("Your female employees seem to be less engaged than their male counterparts. It's important for all employees to feel comfortable speaking up, and lower engagement from a specific group will reduce innovation. Check out our Solutions Tab to solve this problem!")
        inclusion_score = inclusion_score - 1
    elif male_avg_engage < fem_avg_engage:
        print("Your male employees seem to be less engaged than their female counterparts. It's important for all employees to feel comfortable speaking up, and lower engagement from a specific group will reduce innovation. Check out our Solutions Tab to solve this problem!")
        inclusion_score = inclusion_score - 1
    else:
        print("Your employees are equally engaged regardless of gender, but creating a more open, accepting work environement will still benefit engagement overall, so make sure to go to our Solutions Tab for ways to facilitate communication!")

    print("YOUR INCLUSION SCORE: On a scale of 0-7, your inclusion score is " + str(format(inclusion_score)) + ".\n\n")



if __name__ == "__main__":
    diversity("sample_dataset.csv")
    equity("sample_dataset.csv")
    inclusion("sample_dataset.csv")
