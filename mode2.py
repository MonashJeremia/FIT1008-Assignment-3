from landsites import Land
from data_structures.heap import MaxHeap

class Mode2Navigator:
    """
    Mode2Navigator class manages a number of teams with the same number of adventurers
    competing to accumulate the largest score.
    It stimulates a day where each team selects a land site to maximise their score.
    The scores are calculated with the remaining number of adventurers and the gold collected
    from a land site.

    Data Structures and Data Types Used:

    - I used a list data structure to store the list of all the lands that were provided in intialization as this would 
    store each land and allow the stats of each site to be accessible
    - I used a Maxheap data structure to maintain the land sites based on the calculated scores, this allows easy access 
    of the site with the highest score as it would be at the root which can be called with getMax()
    - I used a uple data type to pair the score, remaining adventurers and reward gained with the corresponding site
    to allow heap manipulation to be done 

    Small Examples:
    - For `simulate_day`:
    Given 3 land sites with ratios 4 (400 gold, 100 guardians), 2 (300 gold, 150 guardians), and 1 (100 gold, 100 guardians), and 3 teams with 100 adventurers each:
        - The first team will select the site with a ratio of 4, sending 100 adventurers and collecting 400 gold.
        - The second team will select the site with a ratio of 2, sending 100 adventurers and collecting 200 gold.
        - The third team will select the site with a ratio of 1, sending 100 adventurers and collecting 100 gold.
    If a new site with a ratio of 6 (600 gold, 100 guardians) is added, the next team will prioritize this site over the existing ones.
    
    - For `add_sites`: If a site with 900 gold and 150 guardians is added to the self.sites (a list), it will add this new site into the heap
    maintaining the heap order that is based on largest score

    Complexity Explanations:
    - Explained in each functions
    """

    def __init__(self, n_teams: int) -> None:
        """
        Best and Worst case is O(1) as intialising a integer runs on constant time
        """
        self.n_teams = n_teams # Initialise number of adventurer teams
        self.sites = []
        self.site_heap = None

    def add_sites(self, sites: list[Land]) -> None:
        """
        Best Case is O(S) where S is the number of new sites, as extending the list and heapifying the initial sites are linear
        in the number of new sites.
        Worst Case is O(N + S) where N is the number of existing sites and S is the number of new sites, as it needs to reprocess 
        all existing sites and then the new sites.
        Worst Case can also be considered as O(N) where N is the number of existing sites as well as the new additional sites
        as it processes the new existing sites and additional sites together
        """
        self.sites.extend(sites)  # Extends the list self.sites with any sites given

        site_ratios = [] 
        for site in self.sites:  # For each site in sites
            if site.get_guardians() > 0:  # Check to avoid division by zero
                ratio = site.get_gold() / site.get_guardians()  # Calculate ratio
                site_ratios.append((ratio, site))  # Append ratio with corresponding site

        self.site_heap = MaxHeap(len(site_ratios))  # Initialise the heap
        self.site_heap.heapify(site_ratios)  # Heapify site_heap to reorder the sites

    def compute_score(self, site: Land, adventurer_size: int) -> tuple[float, int, float]:
        """
        Best Case and Worst Case is O(1) as the operations are all calculations that run on constant time
        """
        if site.get_guardians() == 0:
            return float('-inf'), adventurer_size, 0  # Avoid division by zero

        adventurers_sent = min(site.get_guardians(), adventurer_size)
        rewards_earned = min(adventurers_sent * site.get_gold() / site.get_guardians(), site.get_gold())  # Calculates the rewards that can be earned
        remaining_adventurers = adventurer_size - adventurers_sent
        score = (2.5 * remaining_adventurers) + rewards_earned  # Calculates score 
        
        return score, remaining_adventurers, rewards_earned  # Returns values
    
    def construct_score_data_structure(self, adventurer_size: int) -> MaxHeap:
        """
        Best Case is O(N) where N is the number of sites, as when all the sites are originally added it calls 
        heapify to construct the heap which runs in linear time
        Worst Case is O(N*log(N)) where N is the number of sites, as when new sites are inserted it has to go the
        heap has to reheapify which is O(log(N)) and it has to do this O(N) times for the number of new sites added
        """
        site_scores = MaxHeap(len(self.sites))  # Initialise heap for scores

        for site in self.sites:  # For each site
            score, remaining_adventurers, reward_gained = self.compute_score(site, adventurer_size)  # Calculate and return the values
            if score != float('-inf'):  # Only add valid scores
                site_scores.add((score, remaining_adventurers, reward_gained, site))  # Add the stats of a chosen site to site_score
            
        return site_scores # Returns a heap with all the sites stats

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Best Case is O(N) where N is the number of sites, as it would have to construct the score data sctructure
        which is O(N) and then if every team wanted to skip
        Worst Case is O(N + Klog(N)) where N is the number of sites and K is the number of teams, as when each
        team chooses to pick the best site, it would have it would have to construct the score data sctructure
        which is O(N) and for each team (K) extracting the best site, it would have to reheapify the heap
        """
        choices = []  # List to store the choices of each team

        for _ in range(self.n_teams):  # Goes through each team
            best_choice = (None, 0)  # Initialise skipping a turn as default
            max_score = float(0)  # Initialise 0 as max score default

            # If team skips a turn
            remaining_adventurers = adventurer_size # Hold same am of adventurers
            score_if_skip = 2.5 * remaining_adventurers # Calculate score 
            max_score = score_if_skip # Assign that score

            site_stats = self.construct_score_data_structure(adventurer_size) # Construct the score data structure

            if len(site_stats) > 0:
                score, remaining_adventurers, reward_gained, site = site_stats.get_max() # Get site with largest score
                if score > max_score:
                    max_score = score # Assigns the score of the site retrieved
                    best_choice = (site, adventurer_size - remaining_adventurers)
                    site.set_gold(site.get_gold() - reward_gained) # Update sites gold stats
                    site.set_guardians(site.get_guardians() - (adventurer_size - remaining_adventurers)) # Update sites guardian stats

            choices.append(best_choice)  # Add the best choice to the list

        return choices  # Return a list with the site and number of adventurers each team chose
  