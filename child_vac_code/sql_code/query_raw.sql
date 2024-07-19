SELECT [FinancialYearStart]
       ,[Org_Code_ONS] as Org_Code
       ,[Org_Name] as Org_Name_Sub
       ,[Org_Type]
       ,[Data_Type]
       ,[Child_Age]
       ,[Measure] as Vac_Type
       ,[Denominator] as Number_Population
       ,[Value] as Number_Vaccinated
FROM [<Database>].[dbo].[<Table>]
WHERE [FinancialYearStart] = '<FinancialYearStart>'
AND [Measure] not like 'Denom_%'
