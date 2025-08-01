## Modules

Documentation is ongoing. A `*` next to a function parameter indicates optionality. Optional parameters often represent an assumed value, and should still be specified for future-proofing. <br><br>

### genutil

`genutil.extractE9Serial(path_or_filename)`<br>
Given an input path or filename as a string, returns the E9 serial number if one is present. Otherwise, returns a placeholder "E9XXXX".

<br>

`genutil.parseFileSize(size_in_bits)`<br>
Given an input filesize in bits (like that yielded by `os.path.getsize()`), returns a formatted string with the filesize accompanied by its relevant modifier. For example, an input of `12345` would yield `12.34kb`.

<br>

`genutil.compression(filesize_1, filesize_2)`<br>
Given two input filesizes in bits, yields a string-formatted percent reduction between the larger of the two and the smaller.

<br>

`genutil.getColumnData(df, column_name*)`<br>
Given a dataframe and target column name, returns a three-element tuple containing (true column name, column units, full column name with units). The first, second, and third values represent the human-legible name of the column, the associated units of the column, and the full semantically-correct name of the column for use with `df[fullname]` notation, respectively.

If no column name is passed in, returns a list of tuples in the same format, for each column present in the dataframe.

<br>

`genutil.discard(df, preferences, empty*)`<br>
Given an input dataframe and preferences dataframe (df and preferences, respectively), yields a new dataframe with all unwanted columns dropped. If the empty input is provided and set to True, the resultant df also excludes columns detected to be fully empty or 0.

<br>

`genutil.squish(df, preferences)`<br>
Given an input dataframe and preferences dataframe (df and preferences, respectively), yields a new dataframe with a series of compression attempts applied (including trimming of unwanted decimals).

<br>

`genutil.id_patch(keep)`<br>
Given a list of booleans, returns a list of tuples with indices representative of rising/falling edge filter activation. Practically speaking, this is used in conjunction with other GPS processing features to convert a list of datapoint replacements into a list of index ranges.

<br>

`genutil.interp(df, indices)`<br>
Given a dataframe and a list of index ranges (from id_patch), returns a filtered dataframe with values between index ranges linearly interpolated. For use in GPS processing.

<br>

`genutil.gps_filter_data(df)`<br>
Master function which, provided a dataframe input, calculates a variety of metrics and filters incorrect GPS data and returns the resulting dataframe. 

<br>

`genutil.comparativeDF(df, signalA, signalB, asList*, name*)`<br>
Given a dataframe input and two signal names, returns either a dataframe or a list (asList) composed of the relative difference between signalA and signalB. An example of usage might be the relative difference between intercooler temperature out and ambient temperature.

<br>

`genutil.roundcols(df, rounding_accuracy)`<br>
Given a dataframe and a rounding accuracy spec, returns a new dataframe with the specified columns rounded to spec. The rounding accuracy spec should be a dictionary of a similar format to the output of `jsonutil.Prefs.getRoundingAcc`.

<br>

`genutil.parseNames(columns, keys)`<br>
Given a list of dataframe "true" column names, and either a list of keys or a single key, returns a list of "true" column names corresponding to the input keys. If only one key is passed (as a string), a list of one item is returned.

<br>

`genutil.signalFromName(df, name)`<br>
Given a dataframe and a legible signal name, returns the list format of the dataframe's corresponding column data. If the name does not exist in the dataframe, returns an appropriately sized list of 0s.

<br>

`genutil.formatData(df, signal_x, *signals_y)`<br>
Given a dataframe object, a mandatory signal_x value, and (an) optional signal(s)_y value(s), returns either a 1-dimensional array of corresponding data or an N-dimensional array composed of a column of x-data, and N-1 columns of y-data. 

<br>

`genutil.ema(data, *span)`<br>
Given a data object in the form of a 1-D list, returns the exponential moving average filtered result. Defaults to a filter length of 3. Functionally, filter lengths should be tuned to each signal's noise characteristics.

<br>

`genutil.applyFilter(data, *toFilter, *span)`<br>
Applies an ema filter to the provided dataset. Only filters provided columns. If no toFilter list is provided, returns the entire dataset filtered column-wise.<br><br>

### jsonutil

`jsonutil.default_prefs_dir`<br>
Sets the default preferences directory to that packaged in `pvevti`. Can be changed.

**`jsonutil.Prefs`**

> `jsonutil.Prefs.getPrefs(*path)`<br>Given an optional input path, returns a pandas DF object with PD filtering and reduction preferences. <br><br>
> `jsonutil.Prefs.extractUnits(prefs)`<br>Given a preferences DF object, returns a list of tuples in the format (column units, rounding accuracy) where rounding accuracy is an integer expressing number of digits past the decimal to keep.<br><br>
> `jsonutil.Prefs.extractNames(prefs)`<br>Given a preferences DF object, returns a list of tuples in the format (column name, rounding accuracy) where rounding accuracy is an integer expressing number of digits past the decimal to keep.<br><br>
> `jsonutil.Prefs.extractDiscard(prefs)`<br>Given a preferences DF object, returns a list of column names to discard.<br><br>
> `jsonutil.Prefs.columnsToDrop(columns, prefs)`<br>Given a columns list of strings and a prefs input df object, returns a list of true column names from the original DF to drop.<br><br>
> `jsonutil.Prefs.getRoundingAcc(prefs, columns)`<br>Given a prefs input df object and list of columns, returns a dict of keys and values for rounding accuracy to pass into `genutil.roundcols()`.<br><br>

### csvutil

`csvutil.default_csv_dir`<br>The default directory to search for CSV files in for unspecified paths in `csvutil` functions. Is set to the active user's Downloads folder by default.<br><br>

`csvutil.read_csv(filepath)`<br>Returns a pandas DF object of the provided filepath, read using *latin-1* encoding.<br><br>

`csvutil.most_recent_csv(*directory, *ignore, *cascade)`<br>Returns the path to the most recent CSV in the provided directory as a `str`. If none is specified, falls back to the default. If cascade is specified and true, recursively searches all directories contained by the provided directory. If ignore is specified as a string, ignores all CSV files with the provided string in them. <br><br>

`csvutil.all_csvs(directory, *ignore, *cascade)`<br>Yields a `list` of complete paths to CSV files located in the provided directory. If cascade is specified and true, recursively searches all directories contained by the provided directory. If ignore is specified as a string, ignores all CSV files with the provided string in them.<br><br>

`csvutil.df_from_csv(csv_name, *column_names)`<br>Provided a CSV path, yields a DF object. If column_names is specified as a `list`, the DF will only return matching columns. If column_names is unspecified, returns a DF with all columns. Automatically drops all columns with 'Unnamed' in the column name.<br><br>

`csvutil.df_to_csv(df, csv_name, *save_index, *addition)`<br>Provided a DF object, saves a CSV file under the provided name/path. If save_index is provided and true, saves the DF index column in the CSV (most times this is redundant, and defaults to false). If addition is provided and a valid string, appends itself to the save name (an input name of 'C://test.csv' with an addition of '_Filtered' would yield a CSV file at 'C://test_Filtered.csv').<br><br>

### pdfutil

`pdfutil.cols`<br>A list of colors as hex codes (`str`). Modifiable to change the default colors for a plot.<br><br>

`pdfutil.default_config`<br>A dict to specify default PDF configuration. Override with a json import or embed a replacement in a python script. Follows the structure:
```python
{
    "docTitle": "Document Title", "docSubTitle": "Document Subtitle",
    "pages": [
        {
            "pageName": "Page One",
            "plots": [
                {
                    "plotTitle": "Example Plot",
                    "plotType" : "line",
                    "xData"    : "x_axis_data",
                    "yData"    : ["signal_name_1","signal_name_2", "signal_name_3"],
                    "filterLength": 60
                },
                {
                    "plotTitle": "Example Plot 2",
                    "plotType" : "line",
                    "xData"    : "x_axis_data",
                    "yData"    : ["signal_name_4", "signal_name_5"],
                    "filterLength": 300
                }
            ]
        },
        {
            "pageName": "Page Two",
            "plots": [
                {
                    "plotTitle": "Example Plot 3",
                    "plotType" : "scatter",
                    "xData"    : "t",
                    "yData"    : ["signal_name_6", "signal_name_7", "signal_name_8", "signal_name_9"]
                }
            ]
        }
    ]
}
```
<br>

`pdfutil.getCol(i, *colList)`<br>Returns a hex code color for any integer input i. The list defaults to the `pdfutil.cols` list, but can be overridden with a list of any length composed of string hex codes.<br><br>

>**`pdfutil.PDFdoc`**<br>
>`pdfutil.PDFdoc(*name)`<br>Creates an instance of a PDF document object, and a name to save as. If no name is specified, will save under 'Unnamed PDF'.<br><br>
>`pdfutil.PDFdoc.add_page(page)`<br>Attaches a Page object to the PDF document object.<br><br>
>`pdfutil.PDFdoc.save(*location)`<br>Saves the PDF document object to a tangible file on the disc, at the specified location. If no location is specified, defaults to the running directory. <br><br>

<br>

>**`pdfutil.Page`**<br>
>`pdfutil.Page(*title)`<br>Creates an instance of a Page object, and a title to display at the top. If no title is specified, defaults to 'Unnamed Page'.<br><br>
>`pdfutil.Page.set_title(title)`<br>Overwrites plot title.<br><br>
>`pdfutil.Page.add_plot(item)`<br>Adds a Plot object to the Page.<br><br>
>`pdfutil.Page.save_to(pdfObj)`<br>Saves a page to PDF object. Performs layout management and plot rendering.<br><br>

<br>

>**`pdfutil.Plot`**<br>
>`pdfutil.Plot(*type, *data, *legend, *xlabel, *ylabel, *columns, *infer_names)`<br>Creates an instance of a Plot object, with the following optional parameters:
> - `type`: Either 'line' or 'scatter', the type of plot to render.
> - `data`: The conglomerated data, formatted as a list of lists; the first item should be a list of x-axis data, with every item after that a list of signal data.
> - `legend`: Overrides the legend with a list of specified strings. 
> - `xlabel`: String, overrides the x-axis label of the plot.
> - `ylabel`: String, overrides the y-axis label of the plot.
> - `columns`: Either a list of column names or a df.columns object. Only relevant if `infer_names` is true.
> - `infer_names`: Boolean, enables inference of legend content and axis labels based on `columns`.
> 
> <br>
>
> `pdfutil.Plot.infer_names()`<br>Mandates inference of legend and axis labels post-initialization. <br><br>
> `pdfutil.Plot.no_legend()`<br>Clears the legend from the plot.<br><br>
> `pdfutil.Plot.set_legend(legend)`<br>Sets the legend to the provided legend list.<br><br>
> `pdfutil.Plot.no_xlabel()`<br>Clears the x-axis label from the plot.<br><br>
> `pdfutil.Plot.set_xlabel(label)`<br>Sets the x-axis label to the provided string input.<br><br>
> `pdfutil.Plot.no_ylabel()`<br>Clears the y-axis label from the plot.<br><br>
> `pdfutil.Plot.set_ylabel(label)`<br>Sets the y-axis label to the provided string input.<br><br>
> `pdfutil.Plot.no_grid()`<br>Clears all grid properties from the plot.<br><br>
> `pdfutil.Plot.set_grid(label)`<br>Sets the grid status to the provided string input. Options are 'none', 'both', 'x', and 'y'.<br><br>
> `pdfutil.Plot.render()`<br>Renders the plot with the provided settings to the current parent object. Plot settings cannot be altered after rendering.<br><br>

`pdfutil.fixConfig(config)`<br>Corrects a configuration dict to spec and returns the fixed configuration dict; prevents read errors downstream.<br><br>
`pdfutil.createDocument(data, config, *save_path)`<br>Master method to create, manage, and save a document provided inputs:<br>
 - `data`: A pandas DataFrame object containing all relevant data to render. Does not need to be reduced to only the wanted columns.
 - `config`: A config dictionary, preferably corrected with `pdfutil.fixConfig()` which describes plot and page structure, metadata, and save information.
 - `save_path`: An optional string describing the *path* to save to (not filename). It should end in \\.

<br>

## Example Usage

```python
### Technology Demonstrator
#   Showcases the portability of single-lib install and applications.

# Import the pvevti package
import pvevti

# Find the most recent CSV file in the user's downloads folder
csv_file = pvevti.csvutil.most_recent_csv(directory = r"C:\\Users\\USER\\Downloads\\", cascade = True)

# Create a pandas DF using the csv_file path
df = pvevti.csvutil.df_from_csv(csv_file)

# Create a prefs spec from the default preferences (since no path is specified)
prefs = pvevti.jsonutil.Prefs.getPrefs()

# Create and apply a rounding accuracy spec from the prefs spec
rounding_accuracy = pvevti.jsonutil.Prefs.getRoundingAcc(prefs, df.columns)
df = pvevti.genutil.roundCols(df, rounding_accuracy)

# Filter out incomplete GPS data
df = pvevti.genutil.gps_filter_data(df)

# Save the new CSV
pvevti.csvutil.df_to_csv(df, r"C:\\Users\\USER\\Downloads\\")

# Pull the E9 serial number of the CSV file
E9Serial = pvevti.genutil.extractE9Serial(csv_file)

# Acquire the default configuration for the PDF config spec
pdf_config = pvevti.pdfutil.default_config

# Override the document title with the dynamic E9 Serial number
pdf_config["docTitle"] = E9Serial

# Create, manage, and save a PDF document according to the provided spec. By default, saves to C:\\Users\\USER\\
pvevti.pdfutil.createDocument(df, pdf_config)
```