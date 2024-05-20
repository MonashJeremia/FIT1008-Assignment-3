from landsites import Land
from data_structures.heap import MaxHeap




class Mode1Navigator:
    """
    Student-TODO: short paragraph as per
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Best Case is O(1) if one or no landsites were added
        Worst Case is O(N*log(N)) where N is the number of land sites and log(N) is the complexity per insertion operation in a heap
        """
        self.sites = sites
        self.adventurers = adventurers
        self.site_heap = MaxHeap(len(sites))

        for site in sites:
            ratio = site.get_gold() / site.get_guardians()
            self.site_heap.add((ratio, site))

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Best Case is O(log(N)) where N is the number of land sites, as when the initial number of 
        adventurers is less than or equal to the guardians of the first/best site, only one extraction 
        and allocation is needed. log(N) is the height of the heap and the sinking operation takes
        O(log(N)) time.
        Worst Case is O(N) where N is the number of land sites, as when all the the adventurers 
        have to be distributed linearly across multiple sites until all adventurers are distributed
        """
        selected_sites = []
        remaining_adventurers = self.adventurers

        # Initialize a max-heap based on the gold-to-guardians ratio
        heap = MaxHeap(len(self.sites))
        for site in self.sites:
            ratio = site.get_gold() / site.get_guardians()
            heap.add((ratio, site))

        while remaining_adventurers > 0 and len(heap) > 0:
            # Extract the site with the highest gold-to-guardians ratio
            ratio, best_site = heap.get_max()
            max_adventurers_for_site = min(best_site.get_guardians(), remaining_adventurers)
            selected_sites.append((best_site, max_adventurers_for_site))
            remaining_adventurers -= max_adventurers_for_site

        return selected_sites

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Best Case and Worst Case is O(A * N) where A is the length of adventure_numbers and N is the 
        number of land sites, as it would need to iterate through all the sites (N), collating its gold value
        and it would need to iterate through all the adventureres in the adventure_numbers list doing a calculation
        respectively and appending it into the rewards list
        The Best Case and Worst Case is the same as there is no early termination process
        """
        rewards = []

        for num_adventurers in adventure_numbers:
            total_reward = 0
            remaining_adventurers = num_adventurers

            # Allocate adventurers to sites to maximize reward
            for site in self.sites:
                if remaining_adventurers <= 0:
                    break
                max_adventurers_for_site = min(site.get_guardians(), remaining_adventurers)
                total_reward += site.get_gold() * (max_adventurers_for_site / site.get_guardians())
                remaining_adventurers -= max_adventurers_for_site

            rewards.append(total_reward)

        return rewards

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Best Case is O(log(N)) where N is the number of land sites, if the element requires 
        minimal reordering.
        Worst Case is O(N + log(N)) where N is the number of land sites, 
        as locating the element takes O(N) and re-heapifying takes O(log(N)).
        ## INCORRECT COMPLEXITIES WORKS THOUGH
        """
        index = None
        for i in range(1, self.site_heap.length + 1):
            if self.site_heap.the_array[i][1].get_name() == land.get_name():
                index = i
                break

        if index is not None:
            # Update the site’s reward and guardians
            self.site_heap.the_array[index][1].set_gold(new_reward)
            self.site_heap.the_array[index][1].set_guardians(new_guardians)
            new_ratio = new_reward / new_guardians

            # Adjust the heap manually
            self.site_heap.the_array[index] = (new_ratio, self.site_heap.the_array[index][1])
            self.site_heap.rise(index)
            self.site_heap.sink(index)
