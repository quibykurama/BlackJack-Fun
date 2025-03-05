# Blackjack House Odds Analysis

## Overview
This project analyzes the expected value of different starting hands in blackjack for both the player and the house. The calculations are based on probability distributions of possible hands and the house's standing rules. The results are visualized using Python's Matplotlib and Seaborn.

## Features
- Simulates all possible dealer hands up to a defined standing threshold.
- Computes the expected value of each house starting hand.
- Uses probability weighting for realistic odds.
- Visualizes expected values in bar plots.
- Customizable house stand rule (e.g., stand at 15, 16, or 17).

## Installation
To run the project, ensure you have Python installed along with the necessary dependencies. You can install them using:

```bash
pip install numpy pandas matplotlib seaborn
```

## How It Works
1. **Hand Generation:**
   - The script simulates all possible house hands, following blackjack rules.
   - Hands are generated dynamically based on a chosen "stand at" value.

2. **Probability Calculation:**
   - Uses predefined odds for drawing each card value.
   - Computes the likelihood of each possible dealer hand.

3. **Expected Value Computation:**
   - The expected return of each house starting hand is calculated based on possible outcomes.

4. **Visualization:**
   - Generates bar plots displaying the expected values of different starting hands.

## Running the Script
To execute the script, run the following command in your terminal:

```bash
python blackjack_house_odds.py
```

This will generate the expected value calculations and display visualizations.

## Example Output
- The script generates bar charts showing the expected value of house hands given different standing rules.
- Sample visualizations include:
  - Player Stand at 16
  - House Stand at 15
  - House Stand at 17

## Customization
- You can modify the `stand_at` parameter in the script to change house standing rules:
  ```python
  stand_at = 16  # Change this value as needed
  ```
- The script can be extended to analyze **player strategies** by simulating different decision-making heuristics.

## Future Improvements
- Add flexibility for **soft vs. hard standing rules**.
- Implement Monte Carlo simulations for deeper statistical insights.
- Compare expected values across **different blackjack rule variations**.

## Contributing
If you'd like to contribute, feel free to fork this repository and submit a pull request.

## License
This project is open-source and available under the MIT License.

