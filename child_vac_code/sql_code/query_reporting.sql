SELECT [CollectionYearRange]
      ,[Parent_Org_Code]
      ,[Org_Code]
      ,[Org_Name]
      ,[Org_Type]
      ,[Child_Age]
      ,[Vac_Type]
      ,[Vac_Type_Description]
      ,[Data_Type]
      ,[Number_Population]
      ,[Number_Vaccinated]
FROM [<Database>].[dbo].[<Table>]
WHERE [CollectionYearRange] in ('<YearRange>')