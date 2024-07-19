/*
This extracts organisations that were valid as at the end of the financial year
e.g. If 2022-23: organisations that opened before 1st April 2023, and are either
still open, or closed on or after 31st March 2023
If the extract requires organisations that were valid AT ANY TIME during the
financial year, then update the last condition to [DATE_OF_TERMINATION] >= '<FYStart>'
*/
SELECT [GEOGRAPHY_CODE] as Org_Code
      ,[GEOGRAPHY_NAME] as Org_Name
      ,[PARENT_GEOGRAPHY_CODE] as Parent_Org_Code
      ,[ENTITY_CODE] as Entity_code      
      ,[DATE_OF_OPERATION] as Open_date
  FROM [<Database>].[dbo].[<Table>]
  WHERE [ENTITY_CODE] in ('E06','E07','E08','E09','E10','E12','E40','E54')
  AND ([DATE_OF_OPERATION] <= '<FYEnd>' AND ([DATE_OF_TERMINATION] IS NULL OR [DATE_OF_TERMINATION] >= '<FYEnd>'))
ORDER BY Org_code, Open_date
