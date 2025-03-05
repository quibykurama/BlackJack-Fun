import csv
import numpy as np

def calculate_house_hands(stand_at):
    # To store all possible hands
    possible_hands = set()

    # Function to build hands
    def build_hands(stand_at):
        # Start with an initial hand
        current_hand = [11]

        while True:
            # Check if the first card is 0, then break the loop
            if current_hand[-1] == 0:
                break

            # Sum of the current hand
            current_sum = sum(current_hand)
            
            # If the sum of the sequence is 16 or smaller, add 11 as the new card
            if current_sum <= (stand_at - 1):
                current_hand.append(11)
                continue

            # Check if the current sequence meets the conditions
            if stand_at <= current_sum <= 26:
                if (sum(current_hand[:-1]) <= (stand_at -1)) and tuple(current_hand) not in possible_hands and not (sum(current_hand) >= 22 and current_hand[-1] == 11):
                    # Add the hand if it's valid
                    possible_hands.add(tuple(current_hand))
                    #print('#: ' + str(len(possible_hands)) + ' Hand: ' + str(current_hand))

                # Adjust the last card to generate new sequences
                adjust_last_card(current_hand)
                continue

            # Check if the current hand is over 26
            if current_sum >= 27:
                adjust_last_card(current_hand)
                continue
            
    # Function to adjust the last card of the current hand
    def adjust_last_card(current_hand):
        while len(current_hand) >= 2 and current_hand[-1] == 1:
            current_hand.pop()
        if len(current_hand) == 1 and current_hand[-1] == 1:
            current_hand[-1] = 0
        elif current_hand[-1] >= 2:
            current_hand[-1] -= 1

    # Build all possible hands
    build_hands(stand_at)

    # Convert the set of tuples to a list of lists and return it
    list_of_lists = [list(hand) for hand in sorted(possible_hands, reverse=True)]
    return list_of_lists


# Dictionary for the odds per value
val_odds = {
    1: 1/13,
    2: 1/13,
    3: 1/13,
    4: 1/13,
    5: 1/13,
    6: 1/13,
    7: 1/13,
    8: 1/13,
    9: 1/13,
    10: 4/13,
    11: 1/13
}

################## Calculating the real house odds

# Defining Auxiliary Methods Here
# Function to calculate the probability weight of a given hand
def calculate_hand_probability(hand, val_odds):
    # Start with a probability of 1 (since we are multiplying probabilities)
    hand_probability = 1.0

    # Iterate through each value in the hand
    for value in hand:
        # Multiply the cumulative probability by the odds of drawing the current value
        hand_probability *= val_odds.get(value, 0)
    
    return hand_probability

# Function to calculate the total probability weight of a subset of hands
def calculate_subset_probability_weight(hand_dict, val_odds):
    subset_total_weight = 0
    for hands in hand_dict.values():
        subset_total_weight += sum(calculate_hand_probability(hand, val_odds) for hand in hands)
    return subset_total_weight

# Function to calculate odds for a given starting card dictionary (normalized to subset)
def calculate_odds_subset(hand_dict, val_odds):
    # Calculate the total probability weight for the subset
    subset_total_weight = calculate_subset_probability_weight(hand_dict, val_odds)
    
    # Calculate the odds for each outcome by normalizing with the subset total weight
    odds_dict = {}
    for outcome, hands in hand_dict.items():
        outcome_probability_weight = sum(calculate_hand_probability(hand, val_odds) for hand in hands)
        odds_dict[outcome] = outcome_probability_weight / subset_total_weight if subset_total_weight > 0 else 0
    return odds_dict

# Function to calculate the expected value for each starting hand based on outcomes
def calculate_expected_value(odds_df, stand_at):
    expected_values = {}
    
    for _, outcomes in odds_df.iterrows():
        house_hand = outcomes['House Hand']
        expected_value = sum(outcome * outcomes[outcome] for outcome in range(stand_at, 22) if outcome in outcomes)
        expected_values[house_hand] = expected_value
    
    return expected_values

# Function to create a DataFrame from expected values
def create_expected_value_dataframe(expected_values):
    import pandas as pd
    
    expected_values_df = pd.DataFrame(list(expected_values.items()), columns=['House Hand', 'Expected Value'])
    return expected_values_df

# Function to automate the entire process given result data frame and stand_at parameter
def calculate_house_odds(result, val_odds, stand_at):
    import pandas as pd
    
    # Getting the possible hands with set starting values dynamically based on stand_at parameter
    total_hands = {outcome: [hand for hand in result if sum(hand) == outcome] for outcome in range(stand_at, 22)}
    total_hands['BUST'] = [hand for hand in result if sum(hand) > 21]

    # Pre-filter hands based on starting card values to avoid redundant calculations
    filtered_hands_by_start = {}
    for card_value in range(2, 11):
        filtered_hands_by_start[card_value] = [hand for hand in result if hand[0] == card_value]
    # For Ace, filter hands that start with 1 or 11
    filtered_hands_by_start['Ace'] = [hand for hand in result if hand[0] in [1, 11]]

    # Calculate the odds for each subset
    odds_dicts = {}
    for card_value in list(range(2, 11)) + ['Ace']:
        card_label = f'HouseCard {card_value}'
        hand_dict = {outcome: [hand for hand in filtered_hands_by_start[card_value] if sum(hand) == outcome] for outcome in range(stand_at, 22)}
        hand_dict['BUST'] = [hand for hand in filtered_hands_by_start[card_value] if sum(hand) > 21]
        odds_dicts[card_label] = calculate_odds_subset(hand_dict, val_odds)

    # Create the DataFrame from odds dictionaries
    odds_df = pd.DataFrame([{**{'House Hand': k}, **v} for k, v in odds_dicts.items()])
    odds_df['House Hand'] = odds_df['House Hand'].apply(lambda x: x.replace('HouseCard ', ''))
    odds_df = odds_df.sort_values(by='House Hand', key=lambda x: x.map(lambda y: 11 if y == 'Ace' else int(y))).reset_index(drop=True)

    # Calculate expected values for each house starting hand based on outcomes and stand_at parameter
    expected_values = calculate_expected_value(odds_df, stand_at)

    # Create the DataFrame for expected values
    expected_values_df = create_expected_value_dataframe(expected_values)

    return odds_df, expected_values_df


# Call the function with stand_at parameter
stand_at = 17
result = calculate_house_hands(stand_at)
odds_df, expected_values_df = calculate_house_odds(result, val_odds, stand_at)

# Print the DataFrames
print(odds_df)
print(expected_values_df)

# Plot the expected values for each house starting hand
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 8))
sns.barplot(x='House Hand', y='Expected Value', data=expected_values_df, palette='viridis')
plt.title(f'Expected Value for Each House Starting Hand (Stand at {stand_at})')
plt.xlabel('House Starting Hand')
plt.ylabel('Expected Value')
plt.xticks(rotation=45)

# Annotate each bar with the expected value rounded to 3 decimal places
for index, row in expected_values_df.iterrows():
    plt.text(index, row['Expected Value'] + 0.1, f"{row['Expected Value']:.3f}", color='black', ha='center', fontweight='bold')

plt.show()
