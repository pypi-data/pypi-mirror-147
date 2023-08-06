import pandas as pd
import numpy as np
from tqdm import tqdm
import itertools
import argparse
import pickle

import PIconnect as PI

try:
    import OSIsoft
except:
    print("Check queryMultipleTimeFrames function if exists -- Might not be able to find OSIsoft.")

PI.PIConfig.DEFAULT_TIMEZONE = "Australia/Sydney"

SERVER = PI.PIServer()



# <editor-fold desc="Helper Funcitons">
def rollbackTagNames(tag_names, accept_single_name=False):
    if accept_single_name:
        return tag_names.upper().replace("_", ".")
    return [tag_name.upper().replace("_", ".") for tag_name in tag_names]

# Save the object
# Save the object
def savePickle(obj, file_name):
    """
    Save a python object as a .pkl file
    """
    with open(file_name, mode="wb") as file:
        pickle.dump(obj, file)
        file.close()
        print(f"Saved the object to {file_name} successfully!")

# </editor-fold>


# <editor-fold desc="Global Querry Functions">
def getOneInterpolatedTag(tag_name, dates, step_size, periods):
    try:
        tag = SERVER.search(rollbackTagNames(tag_name, True))[0]
    except IndexError as indx_err:
        print(f"{tag_name} couldn't found. Skipping to other tags for Interpolated Values")
        return None, indx_err.__class__.__name__

    one_tag_series = getMultipleInterpolatedDateRanges(tag, dates, step_size, periods)

    return one_tag_series, tag


def getMultipleInterpolatedDateRanges(tag, dates, step_size, periods):
    multiple_range_series = pd.Series(dtype=str)

    for idx, (start_date, end_date) in enumerate(dates):
        single_range_series = getOneInterpolatedDateRange(tag, start_date, end_date, step_size, periods)
        multiple_range_series = multiple_range_series.append(single_range_series)

    return multiple_range_series


def getOneInterpolatedDateRange(tag, start_date, end_date, step_size, periods):
    """by = ["y", "m", "d", "min", "s"] """

    start_date = pd.to_datetime(start_date, infer_datetime_format=True, dayfirst=True, exact=False)
    end_date = pd.to_datetime(end_date, infer_datetime_format=True, dayfirst=True, exact=False)
    dates = pd.date_range(start_date, end_date, periods=periods, tz='Australia/Sydney')

    single_range_series = pd.Series(dtype=str)

    for i in range(len(dates) - 1):
        data = tag.interpolated_values(dates[i], dates[i + 1], step_size)
        single_range_series = single_range_series.append(pd.Series(data.values.astype(str), index=data.index))
        print(f"Finished period {i}!")

    # Remove duplicate dates
    return single_range_series


def getOneRecordedTag(tag_name, dates, periods):
    """ Difference between interpolated and recorded: Recorded sends tag_name to all the way down to  getOneRange """
    try:
        tag = SERVER.search(rollbackTagNames(tag_name, True))[0]
    except IndexError:
        print(f"{tag_name} couldn't found. Skipping to other tags for Recorded values")
        return None

    one_tag_df = getMultipleRecordedDateRanges(tag, tag_name, dates, periods)

    return one_tag_df


def getMultipleRecordedDateRanges(tag, tag_name, dates, periods=4):
    multiple_range_df = pd.DataFrame(columns=["g", "DateTime", "tag_name", "record"])
    for (start_date, end_date) in dates:
        single_range_df = getOneRecordedDateRange(tag, tag_name, start_date, end_date, periods=periods)
        multiple_range_df = multiple_range_df.append(single_range_df, ignore_index=True)

    return multiple_range_df


def getOneRecordedDateRange(tag, tag_name, start_date, end_date, periods=4):
    start_date = pd.to_datetime(start_date, infer_datetime_format=True, dayfirst=True, exact=False)
    end_date = pd.to_datetime(end_date, infer_datetime_format=True, dayfirst=True, exact=False)
    dates = pd.date_range(start_date, end_date, periods=periods, tz='Australia/Sydney')

    single_range_df = pd.DataFrame(columns=["g", "DateTime", "tag_name", "record"])

    for i in range(len(dates) - 1):
        data = tag.recorded_values(dates[i], dates[i + 1])
        single_range_df = single_range_df.append(pd.DataFrame(
            {"g"     : "-1", "DateTime": data.index, "tag_name": tag_name,
             "record": data.values.astype(str)}), ignore_index=True)

    return single_range_df
# </editor-fold>




class Querry():
    def __init__(self, **kwargs):
        """ Tags can be added and subtracted though doesn't let adding new date ranges.
            Create a new instance for that. """
        self.df = pd.DataFrame(columns=["g", "DateTime"])
        self.recording_df = pd.DataFrame(columns=["g", "DateTime", "tag_name", "record"])

        # Expected via kwargs
        self.controllers = []
        self.other_tags = []
        self.dates = []
        self.date_names = []
        self.step_size = None
        self.periods = None
        self.recorded_values = False
        self.interpolated_values = False

        # Gets calculated during operations
        self.continuous = []
        self.categorical = []
        self.all_found_tags = []

        self.found_tag_descriptions = {}
        self.found_tag_dtypes = {}

        self.n_tags = 0
        self.n_records = {}

        for (k, v) in kwargs.items():
            self.__setattr__(k, v)

        self.controllers = [m[0] + "_" + m[1] for m in itertools.product(self.controllers, ["pv", "sv", "mv", "mode"])
                            if m[0] != ""]
        if self.periods == 1:
            self.periods = 2

        self.all_searched_tags = self.controllers + self.other_tags

        # Get the recorded and interpolated values
        if self.recorded_values:
            self.queryRecordings()

        if self.interpolated_values:
            self.querryInterpolatedTags()

    # self.df.reset_index(drop=True, inplace=True)

    def querryInterpolatedTags(self):
        self._querryInterpolatedTags(self.all_searched_tags, self.dates, self.step_size, self.periods)

    def _querryInterpolatedTags(self, tag_names, dates, step_size, periods):
        found_one_tag = False

        tag_idx = 0
        pbar = tqdm(total=len(tag_names))
        # For all tag_names...
        while tag_idx < len(tag_names):
            # ...Try querrying all relavant data
            try:
                one_tag_series, tag = getOneInterpolatedTag(tag_names[tag_idx], dates, step_size, periods)
                one_tag_series = one_tag_series[~one_tag_series.index._duplicated()]

            except AttributeError as attr_err:
                # If tag couldn't found in PI then move to the next one
                if one_tag_series is None and tag == "IndexError":
                    tag_idx +=1
                    pbar.update(1)
                    continue
            # .... If error (Targeting Time out error) -- Then go back and try again the same tag
            # TODO: If Timeout error then catch it here
            except Exception as any_exp:
                print(f"Current exceptions e.__class__.__name__ is {any_exp.__class__.__name__} and below is the actual message:")
                print(any_exp)
                continue

            # If found then add to df and into found tags
            found_one_tag = True
            self._addDataToDF(tag_names[tag_idx], one_tag_series)
            self.df.DateTime = one_tag_series.index
            self.all_found_tags += [tag_names[tag_idx]]
            self.found_tag_descriptions[tag_names[tag_idx]] = tag.description
            self.found_tag_dtypes[tag_names[tag_idx]] = tag.pi_point.PointType
            tag_idx += 1
            pbar.update(1)

        pbar.close()

        if found_one_tag:
            self._setGroupsOfDateTime(interpolated=True)
            self.n_tags = len(self.all_found_tags)


    def queryRecordings(self):
        self._querryRecordings(self.all_searched_tags, self.dates, self.periods)

    def _querryRecordings(self, tag_names, dates, periods):

        # For all tags...
        for tag_name in tqdm(tag_names):
            one_tag_df = getOneRecordedTag(tag_name, dates, periods)
            if one_tag_df is None: continue
            self.recording_df = self.recording_df.append(one_tag_df, ignore_index=True)

        self._setGroupsOfDateTime(interpolated=False)

        self.n_records = dict(self.recording_df.tag_name.value_counts())

    def _addDataToDF(self, tag_name, one_tag_series):
        if self.df.shape[1] != 2:
            assert self.df.shape[0] == one_tag_series.shape[0], "Series and DF doesn't have same number of rows"

        try:
            self.df[tag_name] = one_tag_series.astype("float64")
            self.continuous.append(tag_name)
        except ValueError as err:
            try:
                self.df[tag_name] = one_tag_series.astype(str)
            except:
                one_tag_series.name = tag_name
                self.df = pd.merge(self.df, one_tag_series, how="left", left_index=True, right_index=True)

            self.categorical.append(tag_name)
            print(
                f"While trying to convert {tag_name} to float, BELOW exception is captured and {tag_name} stored as a string")
            print(err)

    def _setGroupsOfDateTime(self, interpolated):
        if interpolated:
            if self.df.shape[0] == 0:
                print("No interpolated data found!")
            else:
                self.df.g = "-1"
                tz = self.df.DateTime.dt.tz
                for idx, (start, end) in enumerate(self.dates):
                    self.df.loc[((self.df.DateTime >= pd.to_datetime(start,infer_datetime_format=True, dayfirst=True, exact=False).tz_localize(tz)) & (
                            self.df.DateTime <= pd.to_datetime(end,infer_datetime_format=True, dayfirst=True, exact=False).tz_localize(tz))),"g"] = \
                        self.date_names[idx]
        else:
            if self.recording_df.shape[0]==0:
                print("No recorded data found!")
            else:
                tz = self.recording_df.DateTime.dt.tz
                for idx, (start, end) in enumerate(self.dates):
                    self.recording_df.loc[
                        ((self.recording_df.DateTime >= pd.to_datetime(start, infer_datetime_format=True, dayfirst=True, exact=False).tz_localize(tz)) & (
                                self.recording_df.DateTime <= pd.to_datetime(end, infer_datetime_format=True, dayfirst=True, exact=False).tz_localize(tz))),"g"] = \
                        self.date_names[idx]

    def addNewTags(self, new_tags):
        if self.interpolated_values:
            assert type(self.df.index[
                            0]) == pd.Timestamp, "To add new tags, indexes should be Timestamp to find matching entries of this new tags"
            if self.periods == 1:
                self.periods = 2

            self._querryInterpolatedTags(new_tags, self.dates, self.step_size, self.periods)

        if self.recorded_values:
            self._querryRecordings(new_tags, self.dates, self.periods)

    # TODO: Convert Querry method to PreProcessor OR find a way to produce processed format of the data
    def addNewDates(self, dates, date_names, step_size, periods):
        d = {"controllers"   : [cont.split("_")[0] for cont in self.controllers],
             "other_tags"    : self.other_tags,
             "dates"         : dates,
             "date_names"    : date_names,
             "step_size"     : step_size,
             "periods"       : periods,
             "recorded_values"  : self.recorded_values,
             }

        q_tmp = Querry(**d)
        new_dates_cols = q_tmp.df.columns.to_list()
        existing_cols = self.df.columns.to_list()

        if step_size != self.step_size:
            print(f"INFO: Initial step size was {self.step_size} and step size for newly added dates is {step_size}")

        if not all([col in new_dates_cols for col in existing_cols]):
            print(
                "Columns are not matching for existing and new dates. Returning Querry object without attaching the queried df to existing one")
            return q_tmp

        self.df = self.df.append(q_tmp.df, ignore_index=True)
        self.df.shape[0]
        print("Appended newly queried dates! Returned Querry object.")
        return q_tmp

    def removeTags(self, tags_to_remove):
        # Remove each tag from list of tags
        for tag in tags_to_remove:
            self.continuous = [cont for cont in self.continuous if cont != tag]
            self.categorical = [cat for cat in self.categorical if cat != tag]

            self.all_found_tags = self.continuous + self.categorical

            if self.n_tags == len(self.all_found_tags):
                print(f"{tag} couldn't found in the tag list")

        # Remove tags from the dataframes
        self.df = self.df[["g", "DateTime"] + self.all_found_tags]
        self.recording_df = self.recording_df.loc[self.recording_df.tag_name.isin(self.all_found_tags),]

    def getNRecordsInTimeRange(self, start_date, end_date):
        """If using string input for dates. Can use following Format 2020-10-20 14:00:00"""
        filtered_df = self.getDateRange(start_date, end_date, interpolated=False, inplace=False)
        n_records = dict(filtered_df.tag_name.value_counts)
        print(n_records)
        return n_records

    def getTags(self, tags: list, interpolated=True):
        # Can only get tags that are found
        tags = [tag for tag in tags if tag in self.all_found_tags]
        if interpolated:
            return self.df[["g", "DateTime"] + tags]
        else:
            return self.recording_df.loc[self.recording_df.tag_name.isin(tags),]

    def getControllers(self, interpolated=True):
        # Can only get tags that are found
        controllers = [tag for tag in self.all_found_tags if tag in self.controllers]
        if interpolated:
            return self.df[controllers]
        else:
            return self.recording_df.loc[self.recording_df.tag_name.isin(controllers),]

    def getOtherTags(self, interpolated=True):
        self.getTags(self.other_tags, interpolated)

    def getContinuous(self, interpolated=True):
        self.getTags(self.continuous, interpolated)

    def getCategorical(self, interpolated=True):
        self.getTags(self.categorical, interpolated)

    def getDateRange(self, start_date, end_date, interpolated=True, inplace=False):
        """If using string input for dates. Can use following Format 2020-10-20 14:00:00"""
        tz = self.df["DateTime"].dt.tz

        if type(start_date) == str:
            start_date = pd.Timestamp(start_date, tz=tz)
        if type(end_date) == str:
            end_date = pd.Timestamp(end_date, tz=tz)

        if interpolated:
            if inplace:
                self.df = self.df.loc[(self.df["DateTime"] > start_date) & (self.df["DateTime"] < end_date),]
                return self.df
            else:
                return self.df.loc[(self.df["DateTime"] > start_date) & (self.df["DateTime"] < end_date),]
        else:
            if inplace:
                self.recording_df = self.recording_df.loc[
                    (self.recording_df["DateTime"] > start_date) & (self.recording_df["DateTime"] < end_date),]
                self.n_records = self.recording_df.shape[0]
            else:
                return self.recording_df.loc[
                    (self.recording_df["DateTime"] > start_date) & (self.recording_df["DateTime"] < end_date),]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="CLI Query Tool")
    # Required Named arguments --
    parser.add_argument("-s","--start_date", nargs="+", help="List of start dates", metavar="", required=True)
    parser.add_argument("-e","--end_date", nargs="+", help="List of end dates", metavar="", required=True)
    parser.add_argument("-t", "--tags", nargs="+", help="List of tags", metavar="", required=True)
    parser.add_argument("-o", "--output_file_name", help="Ouptut .pkl file name", metavar="", required=True)
    parser.add_argument("-i", "--interpolated", help="Flag for NOT getting interpolated data",  action="store_false") # Default True
    parser.add_argument("-r", "--recorded", help="Flag to get recorded data",  action="store_true") # Default False
    parser.add_argument("-st", "--step_size", help="Step size for interpolated data",   required=False, type=str, default="10s")
    parser.add_argument("-p", "--periods", help="Number of groups that the frame will be divided", metavar="", type=int, default=1)
    parser.add_argument("-r", "--recorded", help="Flag to get recorded data",  action="store_true") # Default False

    args = parser.parse_args()

    assert len(args.start_date) == len(args.end_date), "Number of start date & end date entries must be equal"


    d = {"controllers"        : [],
         "other_tags"         : args.tags,
         "dates"              : list(zip(args.start_date, args.end_date)),
         "date_names"         : np.arange(1,len(args.end_date)+1),
         "step_size"          : args.step_size,
         "periods"            : args.periods,
         "alias_mapper"       : {},
         "interpolated_values": args.interpolated,
         "recorded_values"    : args.recorded
         }
    q = Querry(**d)

    # Save output data
    savePickle(q,args.output_file_name)

