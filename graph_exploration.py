import numpy as np
import instaloader


class ProfileNode:
        
    profile = None
    followers = []
    following = []

    def __init__(self, profile):
        
        self.profile = profile
        
        self.userid = profile.userid
        self.username = profile.username
        self.biography = profile.biography
        self.mediacount = profile.mediacount
        self.nb_followers = profile.followers
        self.nb_following = profile.followees
        
        self.is_private = profile.is_private
        self.is_business_account = profile.is_business_account
        self.is_verified = profile.is_verified
        
    def get_followers(self):
        try:
            if not self.is_private:
                print('looking for followers of ', self.username,'...')
                self.followers = [(f.username, f.userid) for f in self.profile.get_followers()]    
        except Exception as e:
            print(e)
            
    def get_following(self):
        try:
            if not self.is_private:
                print('looking for what ', self.username,' follows ...')
                self.following = [(f.username, f.userid) for f in self.profile.get_followees()]
            
        except Exception as e:
            print(e)


def sample_connected_nodes(connected_nodes, max_relatives = 1000):
    n = max(len(connected_nodes), max_relatives)
    return np.random.choice(connected_nodes ,n, replace = False)


def get_relatives(curr_profile, followers = True, following = True):
    
    followers_id = []
    following_id = []
    
    try:
        
        #List followers and Following
        curr_profile.get_followers()
        curr_profile.get_following()
        if followers:
            followers_id = [p[1] for p in curr_profile.followers]
        if following:
            following_id = [p[1] for p in curr_profile.following]
    
    except Exception as e:
        print(e)
        
    return followers_id, following_id

def get_ProfileNode_from_id(profile_id, insta_session):
    
    curr_profile = None
    
    try:
        curr_profile = ProfileNode(instaloader.Profile.from_id(insta_session, profile_id))
        print('process node ', curr_profile.username , '...')
    except Exception as e:
        print(e)
    
    return curr_profile
        




def explore_neighborhood_BFS(root, insta_session, max_nb_explored_profiles = 10000, max_relatives = 100):
    
    """
    from given Instagram profile "root" the function explores all neighboring graph.
    The nbr of maximum nodes is max_nb_explored_profiles
    The nbr of maximum followers or following to be explored is set by max_relatives 
    """
    
    profiles_to_explore = []
    visited = []
    neighboring_network = dict() 
    
    profiles_to_explore.insert(0, root.userid)
    visited.append(root.userid)
    
    while (len(profiles_to_explore) > 0) and (len(visited) < max_nb_explored_profiles):
        
        print('length of profiles to explore = ', len(profiles_to_explore))
        profile_id = profiles_to_explore.pop()
        
        curr_profile = get_ProfileNode_from_id(profile_id, insta_session)
        if curr_profile is not None:
        
            followers_id, following_id = get_relatives(curr_profile)
            
            neighboring_network[curr_profile.userid] = {'username': curr_profile.username,
                                                        'biography' : curr_profile.biography,
                                                        'mediacount' : curr_profile.mediacount, 
                                                        'nb_followers' : curr_profile.nb_followers,
                                                        'nb_following' : curr_profile.nb_following,       
                                                        'is_private' : curr_profile.is_private,
                                                        'is_business_account' : curr_profile.is_business_account,
                                                        'is_verified' : curr_profile.is_verified,
                                                        
                                                        'followers': followers_id,
                                                        'following': following_id}
            
            
            #Select the ones to explore
            followers_sample = sample_connected_nodes(followers_id, max_relatives = max_relatives)
            following_sample = sample_connected_nodes(following_id, max_relatives = max_relatives)
            
            for f in followers_sample:
                if f not in visited:
                    visited.append(f)
                    profiles_to_explore.insert(0,f)
                    
            for f in following_sample:
                if f not in visited:
                    visited.append(f)
                    profiles_to_explore(0,f)
                    
    return neighboring_network
            



